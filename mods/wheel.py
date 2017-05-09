import pymel.core as pm


def addStretchRig(start_ctl, end_ctl, name, ctl_side, main_ctl):
    """
    add wheel stretch with connecting rod rig module.
    :param start_ctl: string
    :param end_ctl: string
    :param name: string
    :param ctl_side: string
    :param main_ctl: string
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
    loc_st = pm.spaceLocator(n='LocDistanceStart_' + name + ctl_side)
    loc_end = pm.spaceLocator(n='LocDistanceEnd_' + name + ctl_side)
    pm.pointConstraint(st_axel_jt, loc_st)
    pm.pointConstraint(end_ctl, loc_end)
    distNode = pm.createNode('distanceBetween', n='distanceBetween' + name, ss=True)
    loc_st.t.connect(distNode.point1)
    loc_end.t.connect(distNode.point2)
    mdn_main_scale = pm.createNode('multiplyDivide', n='multiplyDivideMainScale_' + name + ctl_side)
    mdn_main_scale.operation.set(2)
    distNode.distance.connect(mdn_main_scale.input1X)
    pm.connectAttr(main_ctl + '.scaleY', mdn_main_scale.input2X, f=True)
    mdn = pm.createNode('multiplyDivide', n='multiplyDivide_' + name + ctl_side, ss=True)
    mdn.operation.set(2)
    mdn_main_scale.outputX.connect(mdn.input1X)
    mdn.input2X.set(distNode.distance.get())
    mdn.outputX.connect(st_axel_jt.sx)
    # add skinning joints.
    pm.select(cl=True)
    skinning_joint_start = pm.joint(n=name + '_StartSkinJoint' + ctl_side)
    pm.select(cl=True)
    skinning_joint_end = pm.joint(n=name + '_EndSkinJoint' + ctl_side)
    pm.delete(pm.parentConstraint(start_ctl, skinning_joint_start))
    pm.delete(pm.parentConstraint(end_ctl, skinning_joint_end))
    # parent skin joints.
    pm.parent(skinning_joint_start, st_axel_jt)
    pm.parent(skinning_joint_end, end_axel_jt)
    # aim constraint skin joints.
    pm.aimConstraint(end_ctl, skinning_joint_start, o=[0, 0, 0], w=True, aim=[1, 0, 0], u=[0, 1, 0], wut="vector",
                     wu=[0, 1, 0], mo=False)
    pm.aimConstraint(start_ctl, skinning_joint_end, o=[0, 0, 0], w=True, aim=[1, 0, 0], u=[0, 1, 0], wut="vector",
                     wu=[0, 1, 0], mo=False)
