import datetime
import numpy as np
import streamlit as st

from IPython import display
from concordia import typing
from concordia.agents import basic_agent
from concordia import components as generic_components
from concordia.components.agent import to_be_deprecated as agent_components
from concordia.associative_memory import associative_memory
from concordia.associative_memory import blank_memories
from concordia.associative_memory import formative_memories
from concordia.associative_memory import importance_function
from concordia.language_model import gpt_model
from concordia.clocks import game_clock
from concordia.environment import game_master

GPT_API_KEY = 'lm-studio' #@param {type: 'string'}
GPT_MODEL_NAME = 'TheBloke/Open_Gpt4_8x7B_v0.2-GGUF' #@param {type: 'string'}

if not GPT_API_KEY:
    raise ValueError('GPT_API_KEY is required.')

model = gpt_model.GptLanguageModel(api_key=GPT_API_KEY,
                                   model_name=GPT_MODEL_NAME)

from sentence_transformers import SentenceTransformer
_embedder_model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')
embedder = lambda x: _embedder_model.encode(x, show_progress_bar=False)

START_TIME = datetime.datetime(hour=20, year=2024, month=10, day=1)

MAJOR_TIME_STEP = datetime.timedelta(minutes=30)
MINOR_TIME_STEP = datetime.timedelta(seconds=10)

clock = game_clock.MultiIntervalClock(
    start=START_TIME,
    step_sizes=[MAJOR_TIME_STEP, MINOR_TIME_STEP])

agent_memory = associative_memory.AssociativeMemory(
    sentence_embedder=embedder,
    clock=clock.now,
)

time_alice_wakes_up = START_TIME - datetime.timedelta(hours=12)
agent_memory.add(
    text=(
        'Alice wakes up two hours past her morning alarm after a long night '
        'of being plagued by nightmares. She is late for work.'
    ),
    timestamp=time_alice_wakes_up,
)
time_alice_misses_bus = START_TIME - datetime.timedelta(hours=10)
agent_memory.add(
    text='Alice misses the bus and decides to walk to work.',
    timestamp=time_alice_misses_bus,
)
time_alice_arrives_at_office = START_TIME - datetime.timedelta(hours=8)
agent_memory.add(
    text=(
        'Alice arrives at her office and finds it closed because it\'s '
        'Saturday and her office isn\'t open over the weekends.'
    ),
    timestamp=time_alice_arrives_at_office,
)


class Memories(typing.component.Component):
  """Component that displays recently written memories."""

  def __init__(
      self,
      memory: associative_memory.AssociativeMemory,
      component_name: str = 'memories',
  ):
    """Initializes the component.

    Args:
      memory: Associative memory to add and retrieve observations.
      component_name: Name of this component.
    """
    self._name = component_name
    self._memory = memory

  def name(self) -> str:
    return self._name

  def state(self):
    # Retrieve up to 1000 of the latest memories.
    memories = self._memory.retrieve_recent(k=1000, add_time=True)
    # Concatenate all retrieved memories into a single string and put newline
    # characters ("\n") between each memory.
    return '\n'.join(memories) + '\n'

  def get_last_log(self):
    return {
        'Summary': 'observation',
        'state': self.state().splitlines(),
    }

memory_concatenation_component = Memories(
    memory=agent_memory,
    component_name='memories'
)

agent = basic_agent.BasicAgent(
      model,
      agent_name='Alice',
      clock=clock,
      verbose=True,
      components=[memory_concatenation_component],
      update_interval=MAJOR_TIME_STEP
  )

utterence_from_bob = 'Bob -- "Hey Alice, how has your day been so far?"'
alice_replies = agent.say(utterence_from_bob)
print(alice_replies)

