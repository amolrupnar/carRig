import pymel.core as pm


def filLineEdit(lineEdit, sel=None):
    """
    fill selection in line edit.
    :param lineEdit: string
    :param sel: list
    :return: lineEdit text.
    """
    if not sel:
        sel = pm.ls(sl=True)
    lineEdit.setText(str(sel[0]))
