import unittest
from mock import Mock, patch
import rpm_check


rpmdb = [{'name': 'python', 'version': '2.7', 'release': '1', 'arch': 'x86_64'},
         {'name': 'kernel', 'version': '4.7', 'release': '1', 'arch': 'x86_64'}]


class RpmCheckTest(unittest.TestCase):

    @patch("rpm.TransactionSet.dbMatch", Mock(return_value = iter(rpmdb)))
    def test_pkg_is_installed(self):
       '''Returns list of installed packages'''
       existing_pkgs, missing_pkgs = rpm_check.get_from_rpmdb(["python", "kernel"])
       self.assertEqual(existing_pkgs, ['python-2.7-1-x86_64', 'kernel-4.7-1-x86_64'])

    @patch("rpm.TransactionSet.dbMatch", Mock(return_value = None))
    def test_pkg_is_not_installed(self):
        '''Returns list of missing packages'''
        existing_pkgs, missing_pkgs = rpm_check.get_from_rpmdb(["kenel"])
        self.assertEqual(missing_pkgs, ['kenel'])

    @patch("rpm.TransactionSet.dbMatch")
    def test_one_of_pkgs_is_not_installed(self, mock_db_match):
        '''Returns list of missing packages'''
        mock_db_match.side_effect = [iter(rpmdb), None]
        existing_pkgs, missing_pkgs = rpm_check.get_from_rpmdb(["python", "kenel"])
        self.assertEqual(missing_pkgs, ['kenel'])

    @patch("rpm.TransactionSet.dbMatch")
    def test_check_rpms_is_not_installed(self, mock_db_match):
        '''Calls Ansible fail_json with error if packages are not installed'''
        mock_db_match.side_effect = [iter(rpmdb), None]
        module = Mock()
        rpm_check.check_rpms(module, ["python", "kenel"], 'installed')
        module.fail_json.assert_called_with(msg="No RPMs matching 'kenel' found on system")

    @patch("rpm_check.get_from_rpmdb", return_value=([],['httpd']))
    def test_check_rpms_installed(self, mock_is_installed):
        '''Returns empty Ansible exit_json with 'changed': False if packages are installed'''
        ansible_exit_json = {'msg': '', 'changed': False, 'results': [], 'rc': 0}
        self.assertEqual(rpm_check.check_rpms(Mock(), ["httpd"], 'installed'), ansible_exit_json)