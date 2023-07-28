# Flappy Bird AI using NEAT Algorithm

#### This repository contains an AI-powered Flappy Bird game that utilizes the NEAT (NeuroEvolution of Augmenting Topologies) algorithm to evolve and find the best-performing AI agents to play the game. NEAT is a powerful evolutionary algorithm that allows neural networks to evolve and adapt, making it an excellent fit for training agents to master complex tasks like playing Flappy Bird.

## How the NEAT Algorithm Works

NEAT is a genetic algorithm specially designed for evolving artificial neural networks. It starts with a population of randomly initialized neural networks, where each network represents an AI agent. The AI agents play the Flappy Bird game, and their performance is evaluated based on their ability to navigate the bird through the pipes.

The top-performing AI agents are selected based on their fitness scores, which indicate how well they performed in the game. The selected agents undergo crossover and mutation operations to create new offspring, introducing diversity into the population. The process of selection, crossover, and mutation continues over multiple generations, gradually improving the performance of the AI agents.

## Features

NEAT Algorithm Integration: The NEAT algorithm is seamlessly integrated into the Flappy Bird game to train and evolve AI agents. Users can watch the AI agents improve over generations.

Visualization: The project comes with visualizations to display the performance progress of the AI agents across generations. Users can see how the fitness scores improve over time.

Configurable Parameters: The repository includes configurable parameters for NEAT, allowing users to tweak and experiment with different settings to optimize the AI agent's performance.

## How To Get Started
python3 main.py will start the AI process

python3 flappybird.py will start the game where you can start playing on your own

## Dependency

Python 3.9

Pygame 2.1.3

NEAT-Python
