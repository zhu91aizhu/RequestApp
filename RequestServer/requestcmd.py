# _*_ coding:utf-8 _*_
"""请求命令模块"""

class RequestCmd(object):
    """请求命令类"""

    target_results = {}

    #---------------------------------------------------------------------------
    @classmethod
    def __argument_parser(cls, params):
        """解析参数"""
        from shlex import split
        from argparse import ArgumentParser

        parser = ArgumentParser()
        parser.add_argument("-a", "--append", action="store", \
                dest="append_params")
        parser.add_argument("-r", "--replace", action="store", \
                dest="replace_params")
        parser.add_argument("-d", "--data", action="store_const", \
                dest="is_print", const=True)
        project_group = parser.add_mutually_exclusive_group()
        project_group.add_argument("-c", action="store_const", \
                            dest="project_config", const=True)
        project_group.add_argument("-C", action="store_const", \
                            dest="project_config", const=False)
        parser.add_argument("-i", "--index", action="store", required=True, \
                            dest="request_index", type=int)
        parser.add_argument("-s", "--storage", action="append", \
                            dest="storage", default=[])

        return parser.parse_args(split(params))

    #---------------------------------------------------------------------------
    @classmethod
    def __update_params(cls, results, storage_results, request_entrys, \
            request_index):
        """更新参数字典"""
        append_params = {}
        params_tmp = []
        if results.append_params is not None:
            params_tmp = \
                    results.append_params.replace(" ", "").split(",")
        for param_tmp in params_tmp:
            if param_tmp[0] == '$':
                key = param_tmp[1:]
                value = storage_results[key]
            else:
                param_tmp = param_tmp.split(":")
                key, value = param_tmp
            append_params[key] = value

        src_params = request_entrys[request_index].get_params()
        if src_params is None:
            src_params = {}

        return dict(src_params, **append_params)

    #---------------------------------------------------------------------------
    @classmethod
    def __replace_params(cls, src_params, replace_params):
        """替换请求参数"""
        if replace_params is None:
            return src_params

        # 将请求参数转换成列表
        params = replace_params.replace(" ", "").split(",")
        for param in params:
            data = param.split(":")
            if not src_params.has_key(data[0]):
                print "replace param '%s' is not exists." % data[0]
                continue
            src_params[data[0]] = data[1]

        return src_params

    @classmethod
    def __storage_results(cls, storage, results, keys):
        """存储请求结果"""
        for key in keys:
            if key not in results.keys():
                print "no key is '%s'" % key
            else:
                storage[key] = results[key]

    @classmethod
    def __convert_results(cls, results):
        """转换结果集"""
        for key in results.keys():
            if type(results[key]) is dict:
                RequestCmd.__convert_results(results[key])
            else:
                RequestCmd.target_results[key] = results[key]

    #---------------------------------------------------------------------------
    @classmethod
    def __print_params(cls, is_print, params):
        """打印参数"""
        import urllib

        if is_print is not None:
            print urllib.unquote_plus(params)

    #---------------------------------------------------------------------------
    @classmethod
    def req(cls, req_config, params):
        '''以RequestEntry请求命令'''
        import urllib
        import urllib2
        from json import dumps, loads

        project_config = req_config["project_config"]
        current_project = req_config["current_project"]
        if req_config["current_project"] is None:
            print "no project selected."
            return

        results = RequestCmd.__argument_parser(params)
        request_index = results.request_index - 1
        if results.project_config is not None:
            project_config = results.project_config

        try:
            request_entrys = req_config["request_entrys"]
            if project_config:
                url = current_project.get_project_host() + ":" \
                        + current_project.get_project_port() \
                        + "/" + request_entrys[request_index].get_url()
            else:
                url = request_entrys[request_index].get_url()

            # 更新请求参数
            request_params = RequestCmd.__update_params(results, \
                    req_config["storage"], request_entrys, request_index)
            # 替换请求参数
            request_params = RequestCmd.__replace_params(request_params, \
                    results.replace_params)
            # 转换请求参数
            request_params = urllib.urlencode({
                'data':dumps(request_params)})
            # 打印参数
            RequestCmd.__print_params(results.is_print, request_params)

            try:
                response = urllib2.urlopen(urllib2.Request(url, request_params))
                result = unicode(response.read(), 'utf-8')
                # 转换结果集
                RequestCmd.storage_results = \
                        RequestCmd.__convert_results(loads(result))
                # 存储结果
                RequestCmd.__storage_results(req_config["storage"], \
                        RequestCmd.target_results, results.storage)
                print result
            except ValueError as value_error:
                print "cannot access url or url error.", value_error
        except IndexError as index_error:
            print "req index error.", index_error
        except ValueError as value_error:
            print "limit param error.", value_error
        except urllib2.URLError as url_error:
            print "cannot access url or url error.", url_error
        except Exception:
            print "connect error."
