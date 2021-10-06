from util import routines
from util.agent import VirxERLU, run_bot, Routine, Vector


class DriveInCircle(Routine):
    start_time: float = None

    def run(self, agent: VirxERLU):
        if self.start_time is None:
            self.start_time = agent.time

        agent.controller.steer = 1
        agent.controller.throttle = 1

        if agent.time > self.start_time + 5:
            agent.pop()


class Bot(VirxERLU):
    # If the bot encounters an error, VirxERLU will do it's best to keep the bot from crashing.
    # VirxERLU uses a stack system for it's routines. A stack is a first-in, last-out system of routines.
    # VirxERLU on VirxEC Showcase -> https://virxerlu.virxcase.dev/
    # Questions? Want to be notified about VirxERLU updates? Join my Discord -> https://discord.gg/5ARzYRD2Na
    # Wiki -> https://github.com/VirxEC/VirxERLU/wiki

    def run(self):
        # NOTE This method is ran every tick

        # The bot may or may not be busy with a stack at this point.
        # TODO: if there are any urgent situations that should interrupt the current task,
        # you could do self.clear_task() and then self.push_task(...)

        if not self.has_task():
            # if not self.kickoff_done:
            #     self.push_task(routines.GenericKickoff())
            # else:
            self.push_task(DriveInCircle())
            self.push_task(routines.Goto(Vector(2000, 0, 0)))
            self.push_task(routines.Goto(Vector(0, 0, 0)))
            # TODO: figure out other stuff to do when there's no task

        # At this point, we hopefully have a task.
        if self.has_task():
            self.get_active_task().run(self)
        else:
            # If we never found a task, zero out the throttle and boost so the car stops.
            self.controller.throttle = 0
            self.controller.boost = False


if __name__ == "__main__":
    run_bot(Bot)


############# Polymorphism Example #############
# class Pet:
#     def speak(self):
#         pass
#
# class Dog(Pet):
#     def speak(self):
#         print("woof woof")
#
# class Cat(Pet):
#     def speak(self):
#         print("meow")
#
# if __name__ == "__main__":
#     my_pets: List[Pet] = []
#     my_pets.append(Dog())
#     my_pets.append(Dog())
#     my_pets.append(Dog())
#     my_pets.append(Cat())
#
#     for p in my_pets:
#         p.speak()
