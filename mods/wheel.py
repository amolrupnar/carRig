import pymel.core as pm

startPivot = 'FKFrontWheelRod_L'
endPivot = 'FKfrontWheel_L'
naming = 'FrontWheelAxel'
side = '_L'


def addStretchRig(start_ctl, end_ctl, name, ctl_side):
    """
    add wheel stretch with connecting rod rig module.
    :param start_ctl: string
    :param end_ctl: string
    :param name: string
    :param ctl_side: string
    :return: wheel_rig
    """
    # axel start joint.
    pm.select(cl=True)
    st_axel_jt = pm.joint(n=name + ctl_side)
    pm.delete(pm.parentConstraint(start_ctl, st_axel_jt))
    # axel end joint.
    pm.select(cl=True)
    end_axel_jt = pm.joint(n=name + 'End' + ctl_side)
    pm.delete(pm.parentConstraint(end_ctl, end_axel_jt))
    pm.parent(end_axel_jt, st_axel_jt)
    # axel connector joint.
    pm.select(cl=True)
    axelConnector_jt = pm.joint(n=name + 'Connector' + ctl_side)
    pm.delete(pm.parentConstraint(end_axel_jt, axelConnector_jt))
    pm.pointConstraint(end_axel_jt, axelConnector_jt)
    # parent in start controller.
    pm.parent(st_axel_jt, axelConnector_jt, start_ctl)
    # add ik handle.
    ikHandle = pm.ikHandle(sj=st_axel_jt, ee=end_axel_jt, sol='ikRPsolver', n='IK' + name + ctl_side)
    pm.pointConstraint(end_ctl, ikHandle[0], mo=True)
    # add stretch with main controller.
    loc_st = pm.spaceLocator(n='LocDistanceStart_' + name + side)
    loc_end = pm.spaceLocator(n='LocDistanceEnd_' + name + side)
    pm.pointConstraint(st_axel_jt, loc_st)
    pm.pointConstraint(end_ctl, loc_end)
    distNode = pm.createNode('distanceBetween', n='distanceBetween' + name, ss=True)
    loc_st.t.connect(distNode.point1)
    loc_end.t.connect(distNode.point2)
    mdn = pm.createNode('multiplyDivide', n='multiplyDivide_' + name + ctl_side, ss=True)
    mdn.operation.set(2)
    distNode.distance.connect(mdn.input1X)
    mdn.input2X.set(distNode.distance.get())
    mdn.outputX.connect(st_axel_jt.sx)
