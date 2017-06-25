import pymel.core as pm
import maya.OpenMaya as om


def handStretch(start_ctl, end_ctl, maxPivot, jointStretchy, mainController='Main', name='HandStretch', side='_L',
                addSkinJoints=False):
    """
    add stretch in straight hand.
    :param start_ctl: string
    :param end_ctl: string
    :param maxPivot: string
    :param jointStretchy: string
    :param mainController: string
    :param name: string
    :param side: string
    :param addSkinJoints: bool
    :return: stretchNodes
    """
    # convert all inputs in to PyNode.
    start_ctl = pm.PyNode(start_ctl)
    end_ctl = pm.PyNode(end_ctl)
    maxPivot = pm.PyNode(maxPivot)
    jointStretchy = pm.PyNode(jointStretchy)
    mainController = pm.PyNode(mainController)

    # add stretch with main controller.
    loc_st = pm.spaceLocator(n='LocDistanceStart_' + name + side)
    loc_end = pm.spaceLocator(n='LocDistanceEnd_' + name + side)
    pm.pointConstraint(start_ctl, loc_st)
    pm.pointConstraint(end_ctl, loc_end)
    distNode = pm.createNode('distanceBetween', n='distanceBetween' + name + side, ss=True)
    loc_st.t.connect(distNode.point1)
    loc_end.t.connect(distNode.point2)
    # get max Stretch.
    obj1 = pm.xform(start_ctl, q=True, ws=True, t=True)
    obj2 = pm.xform(maxPivot, q=True, ws=True, t=True)
    posX = obj1[0] - obj2[0]
    posY = obj1[1] - obj2[1]
    posZ = obj1[2] - obj2[2]
    w_dist = om.MVector(posX, posY, posZ)
    maxDistance = w_dist.length()
    # createNode.
    mdn_main_scale = pm.createNode('multiplyDivide', n='multiplyDivide' + name + 'MainScale' + side, ss=True)
    mdn_stretch = pm.createNode('multiplyDivide', n='multiplyDivide' + name + side, ss=True)
    mainController.sy.connect(mdn_main_scale.input1X)
    mdn_main_scale.input2X.set(maxDistance)
    mdn_main_scale.operation.set(1)
    mdn_stretch.operation.set(2)
    distNode.distance.connect(mdn_stretch.input1X)
    mdn_main_scale.outputX.connect(mdn_stretch.input2X)
    # create condition node.
    cond_node = pm.createNode('condition', n='condition' + name + side, ss=True)
    cond_node.operation.set(2)
    distNode.distance.connect(cond_node.firstTerm)
    mdn_main_scale.outputX.connect(cond_node.secondTerm)
    mdn_stretch.outputX.connect(cond_node.colorIfTrueR)
    cond_node.outColorR.connect(jointStretchy.sx)
    if addSkinJoints:
        pm.select(cl=True)
        skinning_joint_start = pm.joint(n=name + '_StartSkinJoint' + side)
        pm.select(cl=True)
        skinning_joint_end = pm.joint(n=name + '_EndSkinJoint' + side)
        pm.delete(pm.parentConstraint(start_ctl, skinning_joint_start))
        pm.delete(pm.parentConstraint(end_ctl, skinning_joint_end))
        # parent skin joints.
        pm.parent(skinning_joint_start, jointStretchy)
        pm.parent(skinning_joint_end, jointStretchy)
        pm.makeIdentity(skinning_joint_start, apply=True, t=1, r=1, s=1, n=0, pn=1)
        pm.makeIdentity(skinning_joint_end, apply=True, t=1, r=1, s=1, n=0, pn=1)
        pm.pointConstraint(end_ctl, skinning_joint_end, mo=True)
