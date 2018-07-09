from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import sys

from rasa_core.agent import Agent
from rasa_core.channels.file import replay_messages
from rasa_core.interpreter import RegexInterpreter


def test_moodbot_example(trained_moodbot_path):
    from rasa_core import run

    agent = Agent.load(trained_moodbot_path)

    responses = agent.handle_text("/greet")
    assert responses[0]['text'] == 'Hey! How are you?'

    responses.extend(agent.handle_text("/mood_unhappy"))
    assert responses[-1]['text'] in {"Did that help you?"}

    # (there is a 'I am on it' message in the middle we are not checking)
    assert len(responses) == 4


def test_restaurantbot_example():
    sys.path.append("examples/restaurantbot/")
    from bot import train_dialogue

    p = "examples/restaurantbot/"
    stories = os.path.join("data", "test_stories", "stories_babi_small.md")
    agent = train_dialogue(os.path.join(p, "restaurant_domain.yml"),
                           os.path.join(p, "models", "dialogue"),
                           stories)

    responses = agent.handle_text("/greet")
    assert responses[0]['text'] == 'how can I help you?'


def test_concerts_online_example():
    sys.path.append("examples/concertbot/")
    from train_online import run_concertbot_online
    from rasa_core import utils

    # simulates cmdline input / detailed explanation above
    utils.input = lambda _=None: "2"

    input_channel = replay_messages(
            'examples/concertbot/data/stories.md',
            message_line_pattern='^\s*\*\s(.*)$',
            max_message_limit=3)
    domain_file = os.path.join("examples", "concertbot", "concert_domain.yml")
    training_file = os.path.join("examples", "concertbot", "data", "stories.md")
    agent = run_concertbot_online(input_channel, RegexInterpreter(),
                                  domain_file, training_file)
    responses = agent.handle_text("/greet")
    assert responses[-1]['text'] in {"hey there!",
                                     "how can I help you?",
                                     "default message"}
