# Copyright (c) 2014 Shotgun Software Inc.
# 
# CONFIDENTIAL AND PROPRIETARY
# 
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit 
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your 
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights 
# not expressly granted therein are reserved by Shotgun Software Inc.

"""
"""

import sgtk
from sgtk.platform.qt import QtCore, QtGui

from .ui.search_widget import Ui_SearchWidget

class SearchWidget(QtGui.QWidget):
    """
    """
    
    search_edited = QtCore.Signal(str)
    search_changed = QtCore.Signal(str)
    
    def __init__(self, parent=None):
        """
        Construction
        """
        QtGui.QWidget.__init__(self, parent)
        
        # set up the UI
        self._ui = Ui_SearchWidget()
        self._ui.setupUi(self)
        
        # dynamically create the clear button so that we can place it over the
        # edit widget:
        self._clear_btn = QtGui.QPushButton(self._ui.search_edit)
        self._clear_btn.setFocusPolicy(QtCore.Qt.StrongFocus)
        self._clear_btn.setFlat(True)
        self._clear_btn.setCursor(QtCore.Qt.ArrowCursor)
        style = ("QPushButton {"
                 + "border: 0px solid;"
                 + "image: url(:/tk-multi-workfiles/clear_search.png);"
                 + "}"
                 + "QPushButton::hover {"
                 + "image: url(:/tk-multi-workfiles/clear_search_hover.png);"
                 + "}")
        self._clear_btn.setStyleSheet(style)
        self._clear_btn.hide()
        
        h_layout = QtGui.QHBoxLayout(self._ui.search_edit)
        h_layout.addStretch()
        h_layout.addWidget(self._clear_btn)
        h_layout.setContentsMargins(3, 0, 3, 0)
        h_layout.setSpacing(0)
        self._ui.search_edit.setLayout(h_layout)

        # hook up the signals:
        self._ui.search_edit.textEdited.connect(self._on_text_edited)
        self._ui.search_edit.returnPressed.connect(self._on_return_pressed)
        self._clear_btn.clicked.connect(self._on_clear_clicked)
                
    # @property
    def _get_search_text(self):
        return self._safe_get_text()
    # @search_text.setter
    def _set_search_text(self, value):
        self._ui.search_edit.setText(value)
    search_text = property(_get_search_text, _set_search_text)
                
    def _on_clear_clicked(self):
        """
        """
        self._ui.search_edit.setText("")
        self.search_changed.emit("")
                
    def _on_text_edited(self):
        """
        """
        text = self._safe_get_text()
        self._clear_btn.setVisible(bool(text))
        self.search_edited.emit(text)
        
    def _on_return_pressed(self):
        """
        """
        self.search_changed.emit(self._safe_get_text())
        
    def _safe_get_text(self):
        """
        """
        text = self._ui.search_edit.text()
        # TODO - handle unicode
        return text
        
        