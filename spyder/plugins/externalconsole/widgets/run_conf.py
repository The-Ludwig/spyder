# -*- coding: utf-8 -*-
#
# Copyright © Spyder Project Contributors
# Licensed under the terms of the MIT License
# (see spyder/__init__.py for details)

"""External console run executor configurations."""

# Standard library imports
import os.path as osp

# Third-party imports
from qtpy.compat import getexistingdirectory
from qtpy.QtWidgets import (
    QWidget, QRadioButton, QGroupBox, QVBoxLayout, QGridLayout,
    QCheckBox, QLineEdit, QHBoxLayout)

# Local imports
from spyder.api.translations import get_translation
from spyder.plugins.run.api import (
    RunExecutorConfigurationGroup, Context, RunConfigurationMetadata)
from spyder.utils.icon_manager import ima
from spyder.utils.misc import getcwd_or_home
from spyder.utils.qthelpers import create_toolbutton

_ = get_translation('spyder')

RUN_DEFAULT_CONFIG = _("Run file with default configuration")
RUN_CUSTOM_CONFIG = _("Run file with custom configuration")
CURRENT_INTERPRETER = _("Execute in current console")
DEDICATED_INTERPRETER = _("Execute in a dedicated console")
SYSTERM_INTERPRETER = _("Execute in an external system terminal")
CLEAR_ALL_VARIABLES = _("Remove all variables before execution")
CONSOLE_NAMESPACE = _("Run in console's namespace instead of an empty one")
POST_MORTEM = _("Directly enter debugging when errors appear")
INTERACT = _("Interact with the Python console after execution")


class ExternalConsolePyConfiguration(RunExecutorConfigurationGroup):
    """External console Python run configuration options."""

    def __init__(self, parent, context: Context,
                 input_extension: str, input_metadata: RunConfigurationMetadata):
        super().__init__(parent, context, input_extension, input_metadata)

        self.dir = None

        # --- Interpreter ---
        interpreter_group = QGroupBox(_("Console"))
        interpreter_layout = QVBoxLayout(interpreter_group)

        # --- System terminal ---
        external_group = QWidget()

        external_layout = QGridLayout()
        external_group.setLayout(external_layout)
        self.interact_cb = QCheckBox(INTERACT)
        external_layout.addWidget(self.interact_cb, 1, 0, 1, -1)

        self.pclo_cb = QCheckBox(_("Command line options:"))
        external_layout.addWidget(self.pclo_cb, 3, 0)
        self.pclo_edit = QLineEdit()
        self.pclo_cb.toggled.connect(self.pclo_edit.setEnabled)
        self.pclo_edit.setEnabled(False)
        self.pclo_edit.setToolTip(_("<b>-u<_b> is added to the "
                                    "other options you set here"))
        external_layout.addWidget(self.pclo_edit, 3, 1)

        interpreter_layout.addWidget(external_group)

        # --- General settings ----
        common_group = QGroupBox(_("General settings"))

        common_layout = QGridLayout(common_group)

        self.clo_cb = QCheckBox(_("Command line options:"))
        common_layout.addWidget(self.clo_cb, 0, 0)
        self.clo_edit = QLineEdit()
        self.clo_cb.toggled.connect(self.clo_edit.setEnabled)
        self.clo_edit.setEnabled(False)
        common_layout.addWidget(self.clo_edit, 0, 1)

        layout = QVBoxLayout(self)
        layout.addWidget(interpreter_group)
        layout.addWidget(common_group)
        layout.addStretch(100)

    def select_directory(self):
        """Select directory"""
        basedir = str(self.wd_edit.text())
        if not osp.isdir(basedir):
            basedir = getcwd_or_home()
        directory = getexistingdirectory(self, _("Select directory"), basedir)
        if directory:
            self.wd_edit.setText(directory)
            self.dir = directory

    def get_default_configuration(self) -> dict:
        return {
            'args_enabled': False,
            'args': '',
            'interact': False,
            'python_args_enabled': False,
            'python_args': '',
        }

    def set_configuration(self, config: dict):
        interact = config['interact']
        args_enabled = config['args_enabled']
        args = config['args']
        py_args_enabled = config['python_args_enabled']
        py_args = config['python_args']

        self.interact_cb.setChecked(interact)
        self.pclo_cb.setChecked(args_enabled)
        self.pclo_edit.setText(args)
        self.clo_cb.setChecked(py_args_enabled)
        self.clo_edit.setText(py_args)

    def get_configuration(self) -> dict:
        return {
            'args_enabled': self.pclo_cb.isChecked(),
            'args': self.pclo_edit.text(),
            'interact': self.interact_cb.isChecked(),
            'python_args_enabled': self.clo_cb.isChecked(),
            'python_args': self.clo_edit.text(),
        }
