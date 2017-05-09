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


class UndoChunkOpen(object):
    def __init__(self, chunkName=''):
        self.chunkName = chunkName

    def __enter__(self):
        pm.undoInfo(cn=self.chunkName, openChunk=True)

    def __exit__(self, exc_type, exc_val, exc_tb):
        pm.undoInfo(cn=self.chunkName, closeChunk=True)
