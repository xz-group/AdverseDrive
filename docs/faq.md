# Frequently Asked Questions (FAQs)

##### What version of Carla did you use?

v0.8.2 [https://github.com/carla-simulator/carla/tree/0.8.2](https://github.com/carla-simulator/carla/tree/0.8.2)

##### What kind of models did you attack?

End-to-end camera based models like [Imitation Learning](https://github.com/carla-simulator/imitation-learning) and [Reinforcement Learning](https://github.com/carla-simulator/reinforcement-learning).

##### How long does it take to run on episode?

10-20 seconds per episode.

##### What ports are used?

By default, the Carla simulator server-client runs port `2000`. This can be changed by modifying the `-world-port=2000` argument while starting the Carla simulator and `--port=2000` argument while running any Python client. The adversary communication takes place over an HTTP port on `8000`. This port currently cannot be changed without repackaging Carla.

##### I keep seeing `[Errno 104] Connection reset by peer` during the experiment. How do I fix it?

This happens because Carla is reset after each episode. At this time, sometimes the client and server lose connection, and this error pops up. We didn't remove it because it is an otherwise important error message when Carla client refuses to communicate with the simulator.

##### How do I contribute to this repo?

Kindly submit a pull request.
