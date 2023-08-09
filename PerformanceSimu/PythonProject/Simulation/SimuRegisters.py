import copy


class SimuReg_routerState:
    '''
    Class used to store the intermediate state of a router.
    '''
    def __init__(self, instance_id="Undefined"):
        '''
        Init
        :param instance_id: string - Default vslue is "Undefined"
        '''
        self.instanceID = instance_id
        self._initializeRegs()

    def _initializeRegs(self):
        '''
        Initialize regs
        :param instance_id:
        :return:
        '''
        self._reg_locked = False
        self._reg_enabledInputPorts = (False, False, False, False, False, False, False)
        self._reg_enabledOutputPorts = (False, False, False, False, False, False, False)
        self._reg_currentFwMode = "wait"

    def getStates_ifRegsLocked(self):
        if self._reg_locked is True:
            return True
        elif self._reg_locked is False:
            return False
        else:
            assert False

    def getStates_inPortsStates(self):
        return copy.deepcopy(self._reg_enabledInputPorts)

    def getStates_outPortsStates(self):
        return copy.deepcopy(self._reg_enabledOutputPorts)

    def getStates_currentFwMode(self):
        return copy.deepcopy(self._reg_currentFwMode)

    def resetStates(self):
        '''
        Reset the regs
        :return:
        '''
        self._initializeRegs()

    def updateStates_lock(self, inPorts_tuple, outPorts_tuple, newFwMode):
        '''
        Update the regs and lock the regs. The values of regs should not be changed until unlocking.
        :return:
        '''
        assert isinstance(inPorts_tuple, tuple) and (len(inPorts_tuple) == 7)
        assert isinstance(outPorts_tuple, tuple) and (len(outPorts_tuple) == 7)
        assert newFwMode in ("wait", "FwUncoded", "FwEncoded", "NCFw")

        assert self.getStates_ifRegsLocked()

        self._reg_enabledInputPorts = copy.deepcopy(inPorts_tuple)
        self._reg_enabledOutputPorts = copy.deepcopy(outPorts_tuple)
        self._reg_currentFwMode = newFwMode

        self._reg_locked = True
