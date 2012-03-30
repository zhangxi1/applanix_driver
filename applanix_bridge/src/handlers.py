import translator
import rospy

from applanix_msgs.msg import Ack


class Handler:
  def handle(self, data):
    raise NotImplementedError


class NullHandler(Handler):
  def handle(self, data):
    pass


class GroupHandler(Handler):
  def __init__(self, name, data_class):
    self.publisher = rospy.Publisher(name, data_class)

  def handle(self, buff):
    msg = self.publisher.data_class()
    msg.translator().deserialize(buff)
    self.publisher.publish(msg)


class MessageHandler(Handler):
  def __init__(self, name, data_class, all_msgs):
    self.name = name
    if data_class.in_all_msgs:
      self.msg = getattr(all_msgs, name) 
    else:
      self.msg = data_class()

    # Keep a reference to the all_msgs aggregate message.
    self.all_msgs = all_msgs

  def handle(self, buff):
    self.msg.translator().deserialize(buff)
    self.all_msgs.last_changed = rospy.get_rostime()


class AckHandler(Handler):
  def __init__(self):
    self.msg = Ack()

  def handle(self, buff):
    self.msg.translator().deserialize(buff)

