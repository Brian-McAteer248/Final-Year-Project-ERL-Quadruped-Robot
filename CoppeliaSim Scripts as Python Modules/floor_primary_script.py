# python

def sysCall_init():
    self.sim = require('sim')


def sysCall_actuation():
    # put your actuation code here
    pass


def sysCall_sensing():
    # put your sensing code here
    pass


def sysCall_cleanup():
    # do some clean-up here
    pass


def remove_and_load_robot_model():
    # Exceptions being thrown here cause CoppeliaSim and terminal connected via remote
    # API to freeze. When beginning experiments, just make sure that robot model is
    # initially available in the scene.
    try:
        torso = self.sim.getObject('/quadruped_robot')
        self.sim.removeModel(torso)
    except Exception as e:
        print('Robot model not already in scene: not calling removeModel()')

    # Load robot model
    torso = self.sim.loadModel(
        'C:/Users/ifiwa/OneDrive/Desktop/4BCT/Final Year Project/(Flat Terrain) Quadruped Robot Model 8 DOF - Shortened Legs.ttm')

    # Return handle to robot script
    return self.sim.getScript(self.sim.scripttype_childscript, torso, '/quadruped_robot')
