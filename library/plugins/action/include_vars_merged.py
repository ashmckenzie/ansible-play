import os
from ansible.utils import template
from ansible import utils
from ansible import errors
from ansible.runner.return_data import ReturnData

class ActionModule(object):
    
    TRANSFERS_FILES = False
    
    def __init__(self, runner):
        self.runner = runner
    
    def run(self, conn, tmp, module_name, module_args, inject, complex_args=None, **kwargs):
        
        if not module_args:
            result = dict(failed=True, msg="No source file given")
            return ReturnData(conn=conn, comm_ok=True, result=result)
        
        source = template.template(self.runner.basedir, module_args, inject)
        
        if '_original_file' in inject:
            source = utils.path_dwim_relative(inject['_original_file'], 'vars', source, self.runner.basedir)
        else:
            source = utils.path_dwim(self.runner.basedir, source)
        
        if os.path.exists(source):
            data = utils.parse_yaml_from_file(source, vault_password=self.runner.vault_pass)
            if data and type(data) != dict:
                raise errors.AnsibleError("%s must be stored as a dictionary/hash" % source)
            elif data is None:
                data = {}
            else:
              data = utils.merge_hash(conn.runner.setup_cache[conn.host], data)
            
            if not hasattr(conn.runner, 'mergeBuffer'):
              conn.runner.mergeBuffer = {}
            
            if conn.host in conn.runner.mergeBuffer:
              data = utils.merge_hash(conn.runner.mergeBuffer[conn.host], data)
            
            conn.runner.mergeBuffer[conn.host] = data
            
            result = dict(ansible_facts=data)
            return ReturnData(conn=conn, comm_ok=True, result=result)
        else:
            result = dict(failed=True, msg="Source file not found.", file=source)
            return ReturnData(conn=conn, comm_ok=True, result=result)
