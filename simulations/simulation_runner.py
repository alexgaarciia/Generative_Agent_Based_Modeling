# Import necessary libraries and components
import concurrent.futures
import datetime
import sentence_transformers
import streamlit as st

from concordia import components as generic_components
from concordia.agents import deprecated_agent as basic_agent
from concordia.components.agent import to_be_deprecated as components
from concordia.associative_memory import associative_memory
from concordia.associative_memory import blank_memories
from concordia.associative_memory import formative_memories
from concordia.associative_memory import importance_function
from concordia.clocks import game_clock
from concordia.components import game_master as gm_components
from concordia.environment import game_master
from concordia.language_model import gpt_model
from concordia.language_model import mistral_model
from concordia.metrics import goal_achievement
from concordia.metrics import common_sense_morality
from concordia.metrics import opinion_of_others
from concordia.thought_chains import thought_chains as thought_chains_lib
from concordia.utils import html as html_lib
from concordia.utils import measurements as measurements_lib


# Setup sentence encoder
st_model = sentence_transformers.SentenceTransformer(
    'sentence-transformers/all-mpnet-base-v2')
embedder = lambda x: st_model.encode(x, show_progress_bar=False)


# Setup LLM
API_KEY = st.session_state.get("api_key", "")
MODEL_NAME = st.session_state.get("selected_model", "")
if MODEL_NAME == "codestral-latest":
    model = model = mistral_model.MistralLanguageModel(api_key=API_KEY, model_name=MODEL_NAME)
else:
    model = gpt_model.GptLanguageModel(api_key=API_KEY, model_name=MODEL_NAME)


# Configure the generic knowledge of players and GM
def create_generic_knowledge(shared_memories):
    shared_memories = st.session_state["shared_context"]
    shared_context = model.sample_text(
        'Summarize the following passage in a concise and insightful fashion:\n'
        + '\n'.join(shared_memories)
        + '\n'
        + 'Summary:'
    )
    return shared_context

importance_model = importance_function.ConstantImportanceModel()
importance_model_gm = importance_function.ConstantImportanceModel()


# Make the clock
TIME_STEP = datetime.timedelta(minutes=20)
SETUP_TIME = datetime.datetime(hour=20, year=2024, month=10, day=1)

START_TIME = datetime.datetime(hour=23, year=2024, month=12, day=27)
clock = game_clock.MultiIntervalClock(
    start=SETUP_TIME,
    step_sizes=[TIME_STEP, datetime.timedelta(seconds=10)])


# Functions to build the players
shared_memories = st.session_state.get("shared_context", [])
blank_memory_factory = blank_memories.MemoryFactory(
    model=model,
    embedder=embedder,
    importance=importance_model.importance,
    clock_now=clock.now,
)

formative_memory_factory = formative_memories.FormativeMemoryFactory(
    model=model,
    shared_memories=shared_memories,
    blank_memory_factory_call=blank_memory_factory.make_blank_memory,
)

def build_agent(agent_config,
                player_names: list[str],
                measurements: measurements_lib.Measurements | None = None):

  mem = formative_memory_factory.make_memories(agent_config)

  agent_name = agent_config.name
  instructions = generic_components.constant.ConstantComponent(
      state=(
          f'The instructions for how to play the role of {agent_name} are as '
          'follows. This is a social science experiment studying how well you '
          f'play the role of a character named {agent_name}. The experiment '
          'is structured as a tabletop roleplaying game (like dungeons and '
          'dragons). However, in this case it is a serious social science '
          'experiment and simulation. The goal is to be realistic. It is '
          f'important to play the role of a person like {agent_name} as '
          f'accurately as possible, i.e., by responding in ways that you think '
          f'it is likely a person like {agent_name} would respond, and taking '
          f'into account all information about {agent_name} that you have. '
          'Always use third-person limited perspective.'
      ),
      name='role playing instructions\n')

  time = generic_components.report_function.ReportFunction(
      name='Current time',
      function=clock.current_time_interval_str,
  )

  current_obs = components.observation.Observation(
            agent_name=agent_config.name,
      clock_now=clock.now,
      memory=mem,
      timeframe=clock.get_step_size(),
      component_name='current observations',
  )
  somatic_state = components.somatic_state.SomaticState(
      model=model,
      memory=mem,
      agent_name=agent_config.name,
      clock_now=clock.now,
  )
  summary_obs = components.observation.ObservationSummary(
      agent_name=agent_config.name,
      model=model,
      clock_now=clock.now,
      memory=mem,
      components=[current_obs],
      timeframe_delta_from=datetime.timedelta(hours=4),
      timeframe_delta_until=datetime.timedelta(hours=1),
      component_name='summary of observations',
  )

  self_perception = components.self_perception.SelfPerception(
      name=f'answer to what kind of person is {agent_config.name}',
      model=model,
      memory=mem,
      agent_name=agent_config.name,
      clock_now=clock.now,
  )
  relevant_memories = components.all_similar_memories.AllSimilarMemories(
      name='relevant memories',
      model=model,
      memory=mem,
      agent_name=agent_name,
      components=[summary_obs, self_perception],
      clock_now=clock.now,
      num_memories_to_retrieve=25,
      verbose=False,
  )
  situation_perception = components.situation_perception.SituationPerception(
      name=(f'answer to what kind of situation is {agent_config.name} in ' +
            'right now'),
      model=model,
      memory=mem,
      agent_name=agent_config.name,
      components=[current_obs, somatic_state, summary_obs],
      clock_now=clock.now,
  )
  person_by_situation = components.person_by_situation.PersonBySituation(
      name=(f'answer to what would a person like {agent_config.name} do in a ' +
            'situation like this'),
      model=model,
      memory=mem,
      agent_name=agent_config.name,
      clock_now=clock.now,
      components=[self_perception, situation_perception],
      verbose=True,
  )

  persona = generic_components.sequential.Sequential(
      name='persona',
      components=[
          self_perception,
          situation_perception,
          person_by_situation,
      ]
  )

  justification_components = components.justify_recent_voluntary_actions
  justification = justification_components.JustifyRecentVoluntaryActions(
      name='justification',
      model=model,
      memory=mem,
      agent_name=agent_config.name,
      components=[persona, somatic_state, relevant_memories],
      clock_now=clock.now,
      verbose=True,
  )
  reflection = components.dialectical_reflection.DialecticalReflection(
      name='reflection',
      model=model,
      memory=mem,
      agent_name=agent_config.name,
      intuition_components=[self_perception, justification],
      thinking_components=[persona],
      clock_now=clock.now,
      num_memories_to_retrieve=5,
      verbose=True,
  )

  initial_goal_component = generic_components.constant.ConstantComponent(
      state=agent_config.goal, name='overarching goal')
  plan = components.plan.SimPlan(
      model,
      mem,
      agent_config.name,
      clock_now=clock.now,
      components=[instructions,
                  initial_goal_component,
                  relevant_memories,
                  persona,
                  justification],
      goal=person_by_situation,
      horizon='the next hour',
      verbose=True,
  )

  goal_metric = goal_achievement.GoalAchievementMetric(
      model=model,
      player_name=agent_config.name,
      player_goal=agent_config.goal,
      clock=clock,
      name='Goal Achievement',
      measurements=measurements,
      channel='goal_achievement',
      verbose=False,
  )
  morality_metric = common_sense_morality.CommonSenseMoralityMetric(
      model=model,
      player_name=agent_config.name,
      clock=clock,
      name='Morality',
      verbose=False,
      measurements=measurements,
      channel='common_sense_morality',
  )
  agent = basic_agent.BasicAgent(
      model,
      agent_name=agent_config.name,
      clock=clock,
      verbose=True,
      components=[instructions,
                  persona,
                  justification,
                  reflection,
                  plan,
                  time,
                  relevant_memories,
                  current_obs,
                  goal_metric,
                  morality_metric],
      update_interval = TIME_STEP
  )
  reputation_metric = opinion_of_others.OpinionOfOthersMetric(
      model=model,
      player_name=agent_config.name,
      player_names=player_names,
      context_fn=agent.state,
      clock=clock,
      name='Opinion',
      verbose=False,
      measurements=measurements,
      channel='opinion_of_others',
      question='What is {opining_player}\'s opinion of {of_player}?',
  )
  agent.add_component(reputation_metric)
  return agent, mem


# Configure and build the players
if 'agents' not in st.session_state:
    st.session_state.agents = []
agents = st.session_state.agents

def create_player_configs(agents):
    return [
        formative_memories.AgentConfig(
            name=agent["name"],
            gender=agent["gender"],
            goal=agent["goal"],
            context=agent["context"],
            traits=agent["traits"],
            formative_ages=agent["formative_ages"],
        )
        for agent in agents
    ]

def build_players(player_configs):   
   num_players = len(player_configs)
   player_goals = {
        player_config.name: player_config.goal for player_config in player_configs}
   players = []
   memories = {}
   measurements = measurements_lib.Measurements()
   
   player_names = [player.name for player in player_configs][:num_players]
   with concurrent.futures.ThreadPoolExecutor(max_workers=num_players) as pool:
    for agent, mem in pool.map(build_agent,
                                player_configs[:num_players],
                                # All players get the same `player_names`.
                                [player_names] * num_players,
                                # All players get the same `measurements` object.
                                [measurements] * num_players):
           players.append(agent)
           memories[agent.name] = mem
    
    return players, memories


def build_gm(players, shared_context):
    game_master_memory = associative_memory.AssociativeMemory(
    sentence_embedder=embedder,
    importance=importance_model_gm.importance,
    clock=clock.now)
    
    # Create components of the Game Master
    player_names = [player.name for player in players]

    scenario_knowledge = generic_components.constant.ConstantComponent(
        state=' '.join(shared_memories),
        name='Background')

    time_display=generic_components.report_function.ReportFunction(
        name='Current time',
        function=clock.current_time_interval_str)

    player_status = gm_components.player_status.PlayerStatus(
        clock_now=clock.now,
        model=model,
        memory=game_master_memory,
        player_names=player_names)

    convo_externality = gm_components.conversation.Conversation(
        players=players,
        model=model,
        memory=game_master_memory,
        clock=clock,
        burner_memory_factory=blank_memory_factory,
        components=[player_status],
        allow_self_talk=True,
        cap_nonplayer_characters=2,
        shared_context=shared_context,
        verbose=True,
    )

    direct_effect_externality = gm_components.direct_effect.DirectEffect(
        players=players,
        model=model,
        memory=game_master_memory,
        clock_now=clock.now,
        verbose=False,
        components=[player_status]
    )

    # Create the game master's thought chain
    account_for_agency_of_others = thought_chains_lib.AccountForAgencyOfOthers(
        model=model, players=players, verbose=False)
    thought_chain = [
        thought_chains_lib.extract_direct_quote,
        thought_chains_lib.attempt_to_most_likely_outcome,
        thought_chains_lib.result_to_effect_caused_by_active_player,
        account_for_agency_of_others,
        thought_chains_lib.restore_direct_quote,
    ]

    # Create the game master object
    env = game_master.GameMaster(
        model=model,
        memory=game_master_memory,
        clock=clock,
        players=players,
        update_thought_chain=thought_chain,
        components=[
            scenario_knowledge,
            player_status,
            convo_externality,
            direct_effect_externality,
            time_display,
        ],
        randomise_initiative=True,
        player_observes_event=False,
        verbose=True,
    )

    return env

def summary(env, players, memories):
    # Check if the logs are already stored in session_state
    if "gm_mem_html" not in st.session_state:
        all_gm_memories = env._memory.retrieve_recent(k=10000, add_time=True)
        gm_mem_html = html_lib.PythonObjectToHTMLConverter(all_gm_memories).convert()
        st.session_state["gm_mem_html"] = gm_mem_html

    if "player_logs" not in st.session_state:
        player_logs = []
        player_log_names = []

        for player in players:
            name = player.name
            detailed_story = '\n'.join(memories[player.name].retrieve_recent(k=1000, add_time=True))
            summary = model.sample_text(
                f'Sequence of events that happened to {name}:\n{detailed_story}'
                '\nWrite a short story that summarises these events.\n',
                max_tokens=8000, terminators=())

            all_player_mem = memories[player.name].retrieve_recent(k=1000, add_time=True)
            all_player_mem = ['Summary:', summary, 'Memories:'] + all_player_mem
            player_html = html_lib.PythonObjectToHTMLConverter(all_player_mem).convert()
            player_logs.append(player_html)
            player_log_names.append(f'{name}')

        # Store the player logs and their names in session_state
        st.session_state["player_logs"] = player_logs
        st.session_state["player_log_names"] = player_log_names

    # Use Streamlit selectbox or radio button for tabs
    selected_tab = st.selectbox("Select a log", ["Game Master"] + st.session_state["player_log_names"])

    # Display the corresponding content for the selected tab
    if selected_tab == "Game Master":
        st.markdown(st.session_state["gm_mem_html"], unsafe_allow_html=True)
    else:
        # Display the selected player's log
        player_index = st.session_state["player_log_names"].index(selected_tab) 
        st.markdown(st.session_state["player_logs"][player_index], unsafe_allow_html=True)
