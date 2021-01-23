from django.test.runner import DiscoverRunner
from unittest import mock
from django.test.utils import get_unique_databases_and_mirrors as _orgin_get_unique_databases_and_mirrors
class NoDbTestRunner(DiscoverRunner):

    def setup_databases(self, **kwargs):
        """ Override the database creation defined in parent class """
        get_unique_databases_and_mirrors = mock.patch('django.test.utils.get_unique_databases_and_mirrors')
        def my_get_unique_databases_and_mirrors():
            test_databases, mirrored_aliases = _orgin_get_unique_databases_and_mirrors()
            out_dc= {}
            for k,v in test_databases.items():
                out_dc[k]=v
                break
            return out_dc,mirrored_aliases
        get_start = get_unique_databases_and_mirrors.start()
        get_start.side_effect = my_get_unique_databases_and_mirrors
        rt =  super().setup_databases(**kwargs)
        get_start.stop()
        return rt

    def teardown_databases(self, old_config, **kwargs):
        """ Override the database teardown defined in parent class """
        pass