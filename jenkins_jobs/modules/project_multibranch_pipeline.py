# -*- coding: utf-8 -*-
# Copyright (C) 2016 Mirantis, Inc.
#
# Based on jenkins_jobs/modules/project_workflow.py by
# Copyright (C) 2015 David Caro <david@dcaro.es>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.


"""
The Pipeline Project module handles creating Jenkins Pipeline projects
(formerly known as the Workflow projects).
You may specify ``pipeline`` in the ``project-type`` attribute of
the :ref:`Job` definition.

Requires the Jenkins :jenkins-wiki:`Pipeline Plugin <Pipeline+Plugin>`:

In order to write an inline script within a job-template you have to escape the
curly braces by doubling them in the DSL: { -> {{ , otherwise it will be
interpreted by the python str.format() command.

:Job Parameters:
    * **remote** (`str`): url to git repo
    * **credentials-id** (`str`): UUID of credentials to use with remote
    * **includes** (`str`): branches to include, space separated list of wildcards
    * **excludes** (`str`): branches to exclude, space separated list of wildcards

"""
import xml.etree.ElementTree as XML

from jenkins_jobs.errors import JenkinsJobsException
import jenkins_jobs.modules.base


class MultiBranchPipeline(jenkins_jobs.modules.base.Base):
    sequence = 0

    def root_xml(self, data):
        xml_parent = XML.Element('org.jenkinsci.plugins.workflow.multibranch.WorkflowMultiBranchProject',
                                 {'plugin': 'workflow-multibranch'})
        xml_sources = XML.SubElement(xml_parent,
                                     'sources',
                                     {'plugin': 'branch-api',
                                      'class': 'jenkins.branch.MultiBranchProject$BranchSourceList'
                                     })
        xml_sources_data = XML.SubElement(xml_sources, 'data')
        xml_branch_source = XML.SubElement(xml_sources_data, 'jenkins.branch.BranchSource')
        xml_source = XML.SubElement(xml_branch_source,
                                     'source',
                                     {'plugin': 'git',
                                      'class': 'jenkins.plugins.git.GitSCMSource'
                                     })
        XML.SubElement(xml_sources, 'owner',
                       {'class': 'org.jenkinsci.plugins.workflow.multibranch.WorkflowMultiBranchProject',
                        'reference': '../..'
                       })
        if 'remote' in data:
            XML.SubElement(xml_source, 'remote').text = data['remote']
        if 'credentials-id' in data:
            XML.SubElement(xml_source, 'credentialsId').text = data['credentials-id']
        if 'includes' in data:
            XML.SubElement(xml_source, 'includes').text = data['includes']
        if 'excludes' in data:
            XML.SubElement(xml_source, 'excludes').text = data['excludes']

        return xml_parent
