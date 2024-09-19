from error_checking.prock_checker import PROCKChecker
from error_checking.oops_checker import OOPSChecker

class ErrorChecker:
    @staticmethod
    def check_prock(ontology_file):
        return PROCKChecker.check(ontology_file)

    @staticmethod
    def check_oops(ontology_file):
        return OOPSChecker.check(ontology_file)