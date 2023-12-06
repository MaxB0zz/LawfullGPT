from panda3d.core import Point3
from direct.showbase.ShowBase import ShowBase


class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        # Load a model and reparent it to render.
        self.environ = self.loader.loadModel("models/environment")
        self.environ.reparentTo(self.render)
        self.wireframe_on()

        # Scale and position the model.
        self.environ.setScale(0.25, 0.25, 0.25)
        self.environ.setPos(-8, 42, 0)

        # Add a task to rotate the camera.
        self.taskMgr.add(self.spin_camera_task, "spin_camera_task")

    def spin_camera_task(self, task):
        angle_degrees = task.time * 6.0
        angle_radians = angle_degrees * (3.14159 / 180.0)
        self.camera.setPos(20 * (angle_degrees % 360), -20 * (angle_degrees % 360), 3)
        self.camera.lookAt(Point3(0, 0, 0))
        return task.cont


if __name__ == "__main__":
    app = MyApp()
    app.run()
