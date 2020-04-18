import json
import os
import sys
from unittest import TestCase

from pbx_gs_python_utils.utils.Dev import Dev
from pbx_gs_python_utils.utils.Files import Files
from pbx_gs_python_utils.utils.Json import Json
from pbx_gs_python_utils.utils.Process import Process
from pbx_gs_python_utils.utils.Unzip_File import Unzip_File
from pbx_gs_python_utils.utils.Zip_Folder import Zip_Folder

from gw_bot.api.gw.sdk_scanner.API_Glasswall_Docker import API_Docker_Glasswall
from gw_bot.api.gw.skd_editor.API_Glasswall_Editor import API_Glasswall_Editor
from gw_bot.api.gw.skd_editor.API_SISL import API_SISL
from gw_bot.helpers.Test_Helper import Test_Helper
from gw_bot.setup.OSBot_Setup import OSBot_Setup
from osbot_browser.view_helpers.Vis_Js import Vis_Js
from osbot_browser.view_helpers.Vis_Js_Views import Vis_Js_Views
from osbot_browser.view_helpers.VivaGraph_Js import VivaGraph_Js
from osbot_browser.view_helpers.VivaGraph_Js_Views import VivaGraph_Js_Views
from osbot_jira.api.graph.GS_Graph import GS_Graph


class test_API_Glasswall_Editor(Test_Helper):
    def setUp(self) -> None:
        super().setUp()
        self.glasswall = API_Glasswall_Editor()
        self.result    = None

    def tearDown(self) -> None:
        if self.result is not None:
            Dev.pprint(self.result)

    def test_ctor(self):
        assert self.glasswall.docker_image == 'glasswallsolutions/evaluationsdk:2'

    def test_glasswall_cli(self):
        #assert self.glasswall.docker_cli(['-v']) == '1.42.33256\nSUCCESS\n'
        self.result =self.glasswall.glasswall_cli(['ls','config'])

    def test_glasswall_scan(self):
        self.result = self.glasswall.glasswall_scan()

    def test_docker_run_bash_command(self):
        assert 'home'                      in self.glasswall.docker_run_bash_command(['ls','/'])
        assert 'glasswallCLI'              in self.glasswall.docker_run_bash_command(['ls'])
        assert 'executable file not found' in self.glasswall.docker_run_bash_command('aaaa')

    def test_scan_file(self):
        file_to_scan = '/tmp/doc-2.docx'
        new_file     = '/tmp/doc-2-NEW.docx'
        self.result = self.glasswall.scan_file(file_to_scan,new_file)

    def test_file_to_sisl(self):
        file_to_scan  = '/tmp/doc-2.docx'
        zip_file = self.glasswall.file_to_sisl(file_to_scan)
        #self.result = zip_file
        self.result = zip_file

    def test_sisl_to_file(self):
        test_folder       = '/tmp/sisl-import-test'
        target_file       = 'doc-2.docx'
        file_to_scan      = f'{test_folder}/{target_file}'                              # Original file to edit
        new_file          = f'{test_folder}/NEW-{target_file}'                          # New file to create
        sisl_stream_id    = '5'                                                         # sisl file that has the content
        sisl_struct_id    = '977'                                                       # location in sisl_stream_id file
        new_text          = 'This IS a NEW content !!!'                                 # new text to go on sisl_struct_id

        glasswall_editor = API_Glasswall_Editor()                                       # API to invoke GW Editor running locally in Docker
        sisl             = API_SISL()                                                   # API to access and manipulate SISL

        sisl_file        = glasswall_editor.file_to_sisl(file_to_scan)                  # GW Engine in Docker to create zip with SISL files (export)
        sisl_folder      = sisl.unzip_sisl_file(sisl_file)                              # extract SISL zip files into temp folder

        sisl.edit_value_array(sisl_folder, sisl_stream_id, sisl_struct_id, new_text)    # to the text replace

        new_sisl_file    = sisl.zip_sisl_files(sisl_folder)                             # zip the SISL files

        glasswall_editor.sisl_to_file(new_sisl_file,new_file)                           # GW Engine in Docker to create new file (import)


    def test_create_mappings_view(self):
        sisl_files = '/tmp/tmpp7dlpszp-doc-2.docx'
        sisl_file = f'{sisl_files}/Id_1857206422_stream_5.sisl'

        sisl = API_SISL()

        results = sisl.create_mappings_view(sisl_file, 1, 10)

        print(f'\nFound: {len(results)}  \n\nKeys : {sorted(list(set(results)))}')

        for key,value in results.items():
            print(key)


    def test_create_graph(self):
        sisl_files = '/tmp/tmpp7dlpszp-doc-2.docx'
        sisl_file  = f'{sisl_files}/Id_1857206422_stream_5.sisl'

        sisl = API_SISL()
        mappings = sisl.mappings(sisl_file,10)

        Dev.pprint(mappings)
        return
        gs_graph = GS_Graph()
        for key, mapping in mappings.items():
            gs_graph.add_node(key,mapping)
            for children in mapping['children']:
                gs_graph.add_edge(key,'',children)

        gs_graph.remove_no_links()

        viva_graph_js = VivaGraph_Js(headless=False)

        nodes = gs_graph.view_nodes(label_key='type',show_key=True, key_id='key')
        edges = gs_graph.edges
        viva_graph_js.create_graph(nodes,edges)


        return
        #viva_graph_js.create_graph(gs_graph['nodes'], gs_graph['edges'])
        #VivaGraph_Js_Views.default(params=[graph_name], headless=False)

        vis_js = Vis_Js(headless=False)
        vis_js.load_page(True)
        # vis_js.options = vis_js.get_advanced_options()
        vis_js.options = { 'nodes': { 'shape' : 'hexagon'          ,
                                      'color' : 'darkblue'         ,
                                      'font'  : {'color': 'black'  ,
                                                 'face' : 'courier',
                                                 'size' : 20    }}}

        (nodes, edges) = gs_graph.view_nodes_and_edges('type',True)
        vis_js.create_graph(nodes, edges)
        #vis_js.show_gs_graph(gs_graph ,label_key='type', show_key=False)

        return


        #vis_js.create_graph(graph['nodes'],graph['edges'])
        #for node in graph['nodes']:
        #    vis_js.add_node(node.get('key'), node.get('label'))

        #for edge in graph['edges']:
        #    vis_js.add_edge(edge['from'], edge['to'])


    def test_visualise_graph(self):
        graph = { 'edges': [ {'from': '0', 'to': '1'},
                             {'from': '1', 'to': '4'},
                             {'from': '1', 'to': '2'},
                             {'from': '4', 'to': '5'},
                             {'from': '5', 'to': '12'},
                             {'from': '5', 'to': '6'}],
                  'nodes': [ {'key': '0'},
                             {'key': '1'},
                             {'key': '4'},
                             {'key': '5'},
                             {'key': '12'},
                             {'key': '11'}]}

        vis_js = Vis_Js(headless=False)
        vis_js.load_page(True)
        for node in graph['nodes']:
            key = node.get('key')
            vis_js.add_node(key,key)

        for edge in graph['edges']:
            vis_js.add_edge(edge['from'], edge['to'])





    def test_view_vis_js_graph(self):
        #OSBot_Setup().setup_test_environment()
        graph_name = 'graph_8MR'
        #vis_js = Vis_Js_Views.default(params         =[graph_name],
        #                              headless       =False       ,
        #                              take_screenshot=False       )
        #vis_js.browser_width(1050)

        vis_js = Vis_Js(headless=False)
        vis_js.load_page(True)
        (vis_js.add_node('1','first node')
               .add_node('2', '2nd node')
               .add_edge('1','2'))


    def test_using_viva_graph(self):
        #OSBot_Setup().setup_test_environment()
        graph_name = 'graph_8MR'
        VivaGraph_Js_Views.default(params=[graph_name], headless=False)

        #vivagraph_js = VivaGraph_Js(headless=False)
        #vivagraph_js.load_page(True)
































    def test_unzip_word_doc(self):
        docx_file    = '/tmp/tmpp7dlpszp-doc-2.docx/doc-2.docx.zip'
        unzip_folder = f'{docx_file}_unziped'

        self.result = Files.unzip_file(docx_file, unzip_folder)





