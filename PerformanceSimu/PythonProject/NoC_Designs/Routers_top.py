# The top designs of Routers
import copy

import Simulation.SimuConfigurationClass as imported_ActiveConfiguration
import Arbiter_Logic.FixedPriority as imported_FixedPriorityArbiter
import Arbiter_Logic.FixedPriority_NC as imported_NCFixedPriorityArbiter


class RoutersTop_BASE:
    '''
    The Base class. Do NOT create the instance of it!

    '''
    def __init__(self, router_id, routerAddr_tuple, SimuConfig_instance):
        assert isinstance(SimuConfig_instance, imported_ActiveConfiguration.SimuConfigs)
        self._SimuConfig_instance = SimuConfig_instance

        assert isinstance(routerAddr_tuple, tuple)
        self._localAddr = copy.deepcopy(routerAddr_tuple)

        self._instanceID = router_id
        self._initializeRegs()
        ##################################################################
        assert False  # You should not create a instance of the base class.
        ##################################################################

    def _initializeRegs(self):
        '''
        Initialize regs
        :return:
        '''
        self._reg_locked = False
        self._reg_enabledInputPorts = (False, False, False, False, False, False, False)
        self._reg_enabledOutputPorts = (False, False, False, False, False, False, False)
        self._reg_currentFwMode = "wait"

    def getConfig_flitBitWidth(self):
        flitBitWidth = self._SimuConfig_instance.getParam_flitBitWidth()
        return copy.deepcopy(flitBitWidth)

    def getStates_localAddr(self):
        return copy.deepcopy(self._localAddr)

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
        assert newFwMode in ("wait", "Fw", "NCFw")

        assert self.getStates_ifRegsLocked()

        self._reg_enabledInputPorts = copy.deepcopy(inPorts_tuple)
        self._reg_enabledOutputPorts = copy.deepcopy(outPorts_tuple)
        self._reg_currentFwMode = newFwMode

        self._reg_locked = True


########################################################################################################################
########################################################################################################################
class RoutersTop_FP(RoutersTop_BASE):
    def __init__(self, router_id, routerAddr_tuple, SimuConfig_instance):
        assert isinstance(SimuConfig_instance, imported_ActiveConfiguration.SimuConfigs)
        self._SimuConfig_instance = SimuConfig_instance

        assert isinstance(routerAddr_tuple, tuple)
        self._localAddr = copy.deepcopy(routerAddr_tuple)

        self._instanceID = router_id
        self._initializeRegs()


    def run_nextCycle(self, fifoStates_tuple, inputReqs_tuple,
                     inputIP_tuple=None, inputW_tuple=None, inputE_tuple=None, inputS_tuple=None, inputN_tuple=None, inputD_tuple=None, inputU_tuple=None):
        '''
        The top design of the router with FixedPriority arbiter.

        :param fifoStates_tuple: tuple(bool, bool, bool, bool, bool, bool, bool) - If the fifos in the output ports of (IP, W, E, S, N, D, U) are available.
        :param inputReqs_tuple: tuple(bool, bool, bool, bool, bool, bool, bool) - If the reqs from (IP, W, E, S, N, D, U) are available.
        :param inputIP_tuple: None or tuple(bool, bool, ...) - A flit. Default value is None.
        :param inputW_tuple: None or tuple(bool, bool, ...) - A flit. Default value is None.
        :param inputE_tuple: None or tuple(bool, bool, ...) - A flit. Default value is None.
        :param inputS_tuple: None or tuple(bool, bool, ...) - A flit. Default value is None.
        :param inputN_tuple: None or tuple(bool, bool, ...) - A flit. Default value is None.
        :param inputD_tuple: None or tuple(bool, bool, ...) - A flit. Default value is None.
        :param inputU_tuple: None or tuple(bool, bool, ...) - A flit. Default value is None.
        :return: currentInPorts_tuple, currentOutPorts_tuple, outIP_tuple, outW_tuple, outE_tuple, outS_tuple, outN_tuple, outD_tuple, outU_tuple
        '''

        assert isinstance(inputReqs_tuple, tuple) and (len(inputReqs_tuple) == 7)
        assert isinstance(fifoStates_tuple, tuple) and (len(fifoStates_tuple) == 7)
        temp_flitBitWidth = self.getConfig_flitBitWidth()
        assert (inputIP_tuple is None) or (
                    isinstance(inputIP_tuple, tuple) and (len(inputIP_tuple) == temp_flitBitWidth))
        assert (inputW_tuple is None) or (
                    isinstance(inputW_tuple, tuple) and (len(inputW_tuple) == temp_flitBitWidth))
        assert (inputE_tuple is None) or (
                    isinstance(inputE_tuple, tuple) and (len(inputE_tuple) == temp_flitBitWidth))
        assert (inputS_tuple is None) or (
                    isinstance(inputS_tuple, tuple) and (len(inputS_tuple) == temp_flitBitWidth))
        assert (inputN_tuple is None) or (
                    isinstance(inputN_tuple, tuple) and (len(inputN_tuple) == temp_flitBitWidth))
        assert (inputD_tuple is None) or (
                    isinstance(inputD_tuple, tuple) and (len(inputD_tuple) == temp_flitBitWidth))
        assert (inputU_tuple is None) or (
                    isinstance(inputU_tuple, tuple) and (len(inputU_tuple) == temp_flitBitWidth))

        # If the current forwarding task is on processing - Continue the current task
        if self.getStates_ifRegsLocked() is True:
            currentInPorts_tuple = self.getStates_inPortsStates()
            currentOutPorts_tuple = self.getStates_outPortsStates()
            currentFwMode = self.getStates_currentFwMode()
            assert currentFwMode == "Fw"

        # If the no task is on processing - Process responses according to the Arbiter alg.
        elif self.getStates_ifRegsLocked() is False:
            # Reqs analyse
            ## IP
            if inputReqs_tuple[0] is True:
                IP_addrA_tuple = copy.deepcopy(
                    self._SimuConfig_instance.flitAnalyse_getAddrA(flit_tuple=copy.deepcopy(inputIP_tuple)))
                IP_addrB_tuple = copy.deepcopy(
                    self._SimuConfig_instance.flitAnalyse_getAddrB(flit_tuple=copy.deepcopy(inputIP_tuple)))
                reqIP_tuple = (True, IP_addrA_tuple[0], IP_addrA_tuple[1], IP_addrA_tuple[2])
                assert self._SimuConfig_instance.flitAnalyse_getType(flit_tuple=copy.deepcopy(inputIP_tuple)) == "head"
            elif inputReqs_tuple[0] is False:
                reqIP_tuple = (False, 0, 0, 0)
            else:
                assert False

            ## W
            if inputReqs_tuple[1] is True:
                W_addrA_tuple = copy.deepcopy(
                    self._SimuConfig_instance.flitAnalyse_getAddrA(flit_tuple=copy.deepcopy(inputW_tuple)))
                W_addrB_tuple = copy.deepcopy(
                    self._SimuConfig_instance.flitAnalyse_getAddrB(flit_tuple=copy.deepcopy(inputW_tuple)))
                reqW_tuple = (True, W_addrA_tuple[0], W_addrA_tuple[1], W_addrA_tuple[2])
                assert self._SimuConfig_instance.flitAnalyse_getType(flit_tuple=copy.deepcopy(inputW_tuple)) == "head"
            elif inputReqs_tuple[1] is False:
                reqW_tuple = (False, 0, 0, 0)
            else:
                assert False

            ## E
            if inputReqs_tuple[2] is True:
                E_addrA_tuple = copy.deepcopy(
                    self._SimuConfig_instance.flitAnalyse_getAddrA(flit_tuple=copy.deepcopy(inputE_tuple)))
                E_addrB_tuple = copy.deepcopy(
                    self._SimuConfig_instance.flitAnalyse_getAddrB(flit_tuple=copy.deepcopy(inputE_tuple)))
                reqE_tuple = (True, E_addrA_tuple[0], E_addrA_tuple[1], E_addrA_tuple[2])
                assert self._SimuConfig_instance.flitAnalyse_getType(flit_tuple=copy.deepcopy(inputE_tuple)) == "head"
            elif inputReqs_tuple[2] is False:
                reqE_tuple = (False, 0, 0, 0)
            else:
                assert False

            ## S
            if inputReqs_tuple[3] is True:
                S_addrA_tuple = copy.deepcopy(
                    self._SimuConfig_instance.flitAnalyse_getAddrA(flit_tuple=copy.deepcopy(inputS_tuple)))
                S_addrB_tuple = copy.deepcopy(
                    self._SimuConfig_instance.flitAnalyse_getAddrB(flit_tuple=copy.deepcopy(inputS_tuple)))
                reqS_tuple = (True, S_addrA_tuple[0], S_addrA_tuple[1], S_addrA_tuple[2])
                assert self._SimuConfig_instance.flitAnalyse_getType(flit_tuple=copy.deepcopy(inputS_tuple)) == "head"
            elif inputReqs_tuple[3] is False:
                reqS_tuple = (False, 0, 0, 0)
            else:
                assert False

            ## N
            if inputReqs_tuple[4] is True:
                N_addrA_tuple = copy.deepcopy(
                    self._SimuConfig_instance.flitAnalyse_getAddrA(flit_tuple=copy.deepcopy(inputN_tuple)))
                N_addrB_tuple = copy.deepcopy(
                    self._SimuConfig_instance.flitAnalyse_getAddrB(flit_tuple=copy.deepcopy(inputN_tuple)))
                reqN_tuple = (True, N_addrA_tuple[0], N_addrA_tuple[1], N_addrA_tuple[2])
                assert self._SimuConfig_instance.flitAnalyse_getType(flit_tuple=copy.deepcopy(inputN_tuple)) == "head"
            elif inputReqs_tuple[4] is False:
                reqN_tuple = (False, 0, 0, 0)
            else:
                assert False

            ## D
            if inputReqs_tuple[5] is True:
                D_addrA_tuple = copy.deepcopy(
                    self._SimuConfig_instance.flitAnalyse_getAddrA(flit_tuple=copy.deepcopy(inputD_tuple)))
                D_addrB_tuple = copy.deepcopy(
                    self._SimuConfig_instance.flitAnalyse_getAddrB(flit_tuple=copy.deepcopy(inputD_tuple)))
                reqD_tuple = (True, D_addrA_tuple[0], D_addrA_tuple[1], D_addrA_tuple[2])
                assert self._SimuConfig_instance.flitAnalyse_getType(flit_tuple=copy.deepcopy(inputD_tuple)) == "head"
            elif inputReqs_tuple[5] is False:
                reqD_tuple = (False, 0, 0, 0)
            else:
                assert False

            ## U
            if inputReqs_tuple[6] is True:
                U_addrA_tuple = copy.deepcopy(
                    self._SimuConfig_instance.flitAnalyse_getAddrA(flit_tuple=copy.deepcopy(inputU_tuple)))
                U_addrB_tuple = copy.deepcopy(
                    self._SimuConfig_instance.flitAnalyse_getAddrB(flit_tuple=copy.deepcopy(inputU_tuple)))
                reqU_tuple = (True, U_addrA_tuple[0], U_addrA_tuple[1], U_addrA_tuple[2])
                assert self._SimuConfig_instance.flitAnalyse_getType(flit_tuple=copy.deepcopy(inputU_tuple)) == "head"
            elif inputReqs_tuple[6] is False:
                reqU_tuple = (False, 0, 0, 0)
            else:
                assert False

            # Arbiter
            currentInPorts_tuple, currentOutPorts_tuple = imported_FixedPriorityArbiter.arbiterLogic_fixedPriority(addrLocal_tuple=self.getStates_localAddr(),
                                                                                                           fifoStates_tuple=copy.deepcopy(fifoStates_tuple),
                                                                                                           reqIP_tuple=copy.deepcopy(reqIP_tuple),
                                                                                                           reqW_tuple=copy.deepcopy(reqW_tuple),
                                                                                                           reqE_tuple=copy.deepcopy(reqE_tuple),
                                                                                                           reqS_tuple=copy.deepcopy(reqS_tuple),
                                                                                                           reqN_tuple=copy.deepcopy(reqN_tuple),
                                                                                                           reqD_tuple=copy.deepcopy(reqD_tuple),
                                                                                                           reqU_tuple=copy.deepcopy(reqU_tuple))
            currentFwMode = "Fw"

        else:
            assert False

        # Forwarding####################################################################################################
        # Mode 1: Forwarding one UNCODED packet
        switch_flitIn = None
        switch_flitInCount = 0
        # IP in
        if currentInPorts_tuple[0] is True:
            switch_flitIn = copy.deepcopy(inputIP_tuple)
            switch_flitInCount = switch_flitInCount + 1
            assert inputReqs_tuple[0] is True

        # W in
        if currentInPorts_tuple[1] is True:
            switch_flitIn = copy.deepcopy(inputW_tuple)
            switch_flitInCount = switch_flitInCount + 1
            assert inputReqs_tuple[1] is True

        # E in
        if currentInPorts_tuple[2] is True:
            switch_flitIn = copy.deepcopy(inputE_tuple)
            switch_flitInCount = switch_flitInCount + 1
            assert inputReqs_tuple[2] is True

        # S in
        if currentInPorts_tuple[3] is True:
            switch_flitIn = copy.deepcopy(inputS_tuple)
            switch_flitInCount = switch_flitInCount + 1
            assert inputReqs_tuple[3] is True

        # N in
        if currentInPorts_tuple[4] is True:
            switch_flitIn = copy.deepcopy(inputN_tuple)
            switch_flitInCount = switch_flitInCount + 1
            assert inputReqs_tuple[4] is True

        # D in
        if currentInPorts_tuple[5] is True:
            switch_flitIn = copy.deepcopy(inputD_tuple)
            switch_flitInCount = switch_flitInCount + 1
            assert inputReqs_tuple[5] is True

        # U in
        if currentInPorts_tuple[6] is True:
            switch_flitIn = copy.deepcopy(inputU_tuple)
            switch_flitInCount = switch_flitInCount + 1
            assert inputReqs_tuple[6] is True

        switch_flitOutCount = 0

        # IP out
        if currentOutPorts_tuple[0] is True:
            outIP_tuple = copy.deepcopy(switch_flitIn)
            switch_flitOutCount = switch_flitOutCount + 1
            assert fifoStates_tuple[0] is True
        elif currentOutPorts_tuple[0] is False:
            outIP_tuple = None
        else:
            assert False

        # W out
        if currentOutPorts_tuple[1] is True:
            outW_tuple = copy.deepcopy(switch_flitIn)
            switch_flitOutCount = switch_flitOutCount + 1
            assert fifoStates_tuple[1] is True
        elif currentOutPorts_tuple[1] is False:
            outW_tuple = None
        else:
            assert False

        # E out
        if currentOutPorts_tuple[2] is True:
            outE_tuple = copy.deepcopy(switch_flitIn)
            switch_flitOutCount = switch_flitOutCount + 1
            assert fifoStates_tuple[2] is True
        elif currentOutPorts_tuple[2] is False:
            outE_tuple = None
        else:
            assert False

        # S out
        if currentOutPorts_tuple[3] is True:
            outS_tuple = copy.deepcopy(switch_flitIn)
            switch_flitOutCount = switch_flitOutCount + 1
            assert fifoStates_tuple[3] is True
        elif currentOutPorts_tuple[3] is False:
            outS_tuple = None
        else:
            assert False

        # N out
        if currentOutPorts_tuple[4] is True:
            outN_tuple = copy.deepcopy(switch_flitIn)
            switch_flitOutCount = switch_flitOutCount + 1
            assert fifoStates_tuple[4] is True
        elif currentOutPorts_tuple[4] is False:
            outN_tuple = None
        else:
            assert False

        # D out
        if currentOutPorts_tuple[5] is True:
            outD_tuple = copy.deepcopy(switch_flitIn)
            switch_flitOutCount = switch_flitOutCount + 1
            assert fifoStates_tuple[5] is True
        elif currentOutPorts_tuple[5] is False:
            outD_tuple = None
        else:
            assert False

        # U out
        if currentOutPorts_tuple[6] is True:
            outU_tuple = copy.deepcopy(switch_flitIn)
            switch_flitOutCount = switch_flitOutCount + 1
            assert fifoStates_tuple[6] is True
        elif currentOutPorts_tuple[6] is False:
            outU_tuple = None
        else:
            assert False

        # Post process
        if self.getStates_ifRegsLocked() is True:
            assert switch_flitOutCount == 1
            assert switch_flitInCount == 1

            # Update the router states (regs) according to the flit processed.
            switch_flitIn_flitType = self._SimuConfig_instance.flitAnalyse_getType(flit_tuple=copy.deepcopy(switch_flitIn))
            assert switch_flitIn_flitType in ("payload", "tail")
            if switch_flitIn_flitType == "tail":
                self.resetStates()

        elif self.getStates_ifRegsLocked() is False:
            assert switch_flitOutCount in (0, 1)
            assert switch_flitInCount in (0, 1)

            # Update the router states (regs) according to the flit processed.
            if switch_flitInCount == 1:
                switch_flitIn_flitType = self._SimuConfig_instance.flitAnalyse_getType(flit_tuple=copy.deepcopy(switch_flitIn))
                assert switch_flitIn_flitType == "head"
                assert switch_flitOutCount == 1
                self.updateStates_lock(inPorts_tuple=copy.deepcopy(currentInPorts_tuple), outPorts_tuple=copy.deepcopy(currentOutPorts_tuple), newFwMode=copy.deepcopy(currentFwMode))

        # Return
        return copy.deepcopy(currentInPorts_tuple), copy.deepcopy(currentOutPorts_tuple), copy.deepcopy(outIP_tuple), copy.deepcopy(outW_tuple), copy.deepcopy(outE_tuple), copy.deepcopy(outS_tuple), copy.deepcopy(outN_tuple), copy.deepcopy(outD_tuple), copy.deepcopy(outU_tuple)


########################################################################################################################
########################################################################################################################
class RoutersTop_NCFP(RoutersTop_BASE):
    def __init__(self, router_id, routerAddr_tuple, SimuConfig_instance):
        assert isinstance(SimuConfig_instance, imported_ActiveConfiguration.SimuConfigs)
        self._SimuConfig_instance = SimuConfig_instance

        assert isinstance(routerAddr_tuple, tuple)
        self._localAddr = copy.deepcopy(routerAddr_tuple)

        self._instanceID = router_id
        self._initializeRegs()

    def XORNC_encodingHeadFlits(self, flit_A, flit_B):
        flit_AddrLenX = self._SimuConfig_instance.getParam_flitAddrBitWidth_X()
        flit_AddrLenY = self._SimuConfig_instance.getParam_flitAddrBitWidth_Y()
        flit_AddrLenZ = self._SimuConfig_instance.getParam_flitAddrBitWidth_Z()
        flit_AddrLenXYZ = flit_AddrLenX + flit_AddrLenY + flit_AddrLenZ

        flitA_Type = self._SimuConfig_instance.flitAnalyse_getType(flit_tuple=copy.deepcopy(flit_A))
        flitB_Type = self._SimuConfig_instance.flitAnalyse_getType(flit_tuple=copy.deepcopy(flit_B))
        assert (flitA_Type == "head") and (flitB_Type == "head")
        flitA_len = len(flit_A)
        assert flitA_len == len(flit_B)

        flitEncoded_list = flitA_len * [False]
        flitEncoded_list[0] = True
        flitEncoded_list[1] = True
        flitEncoded_list[2] = False
        idx_flit_i = 3
        for idx_ii in range(0, flit_AddrLenXYZ):
            flitEncoded_list[idx_flit_i] = flit_A[idx_flit_i]
            flitEncoded_list[idx_flit_i + flit_AddrLenXYZ] = flit_B[idx_flit_i]
            idx_flit_i = idx_flit_i + 1

        return tuple(flitEncoded_list)


    def run_nextCycle(self, fifoStates_tuple, inputReqs_tuple,
                     inputIP_tuple=None, inputW_tuple=None, inputE_tuple=None, inputS_tuple=None, inputN_tuple=None, inputD_tuple=None, inputU_tuple=None):
        '''
        The top design of the router with FixedPriority arbiter.

        :param fifoStates_tuple: tuple(bool, bool, bool, bool, bool, bool, bool) - If the fifos in the output ports of (IP, W, E, S, N, D, U) are available.
        :param inputReqs_tuple: tuple(bool, bool, bool, bool, bool, bool, bool) - If the reqs from (IP, W, E, S, N, D, U) are available.
        :param inputIP_tuple: None or tuple(bool, bool, ...) - A flit. Default value is None.
        :param inputW_tuple: None or tuple(bool, bool, ...) - A flit. Default value is None.
        :param inputE_tuple: None or tuple(bool, bool, ...) - A flit. Default value is None.
        :param inputS_tuple: None or tuple(bool, bool, ...) - A flit. Default value is None.
        :param inputN_tuple: None or tuple(bool, bool, ...) - A flit. Default value is None.
        :param inputD_tuple: None or tuple(bool, bool, ...) - A flit. Default value is None.
        :param inputU_tuple: None or tuple(bool, bool, ...) - A flit. Default value is None.
        :return: currentInPorts_tuple, currentOutPorts_tuple, outIP_tuple, outW_tuple, outE_tuple, outS_tuple, outN_tuple, outD_tuple, outU_tuple
        '''

        assert isinstance(inputReqs_tuple, tuple) and (len(inputReqs_tuple) == 7)
        assert isinstance(fifoStates_tuple, tuple) and (len(fifoStates_tuple) == 7)
        temp_flitBitWidth = self.getConfig_flitBitWidth()
        assert (inputIP_tuple is None) or (
                    isinstance(inputIP_tuple, tuple) and (len(inputIP_tuple) == temp_flitBitWidth))
        assert (inputW_tuple is None) or (
                    isinstance(inputW_tuple, tuple) and (len(inputW_tuple) == temp_flitBitWidth))
        assert (inputE_tuple is None) or (
                    isinstance(inputE_tuple, tuple) and (len(inputE_tuple) == temp_flitBitWidth))
        assert (inputS_tuple is None) or (
                    isinstance(inputS_tuple, tuple) and (len(inputS_tuple) == temp_flitBitWidth))
        assert (inputN_tuple is None) or (
                    isinstance(inputN_tuple, tuple) and (len(inputN_tuple) == temp_flitBitWidth))
        assert (inputD_tuple is None) or (
                    isinstance(inputD_tuple, tuple) and (len(inputD_tuple) == temp_flitBitWidth))
        assert (inputU_tuple is None) or (
                    isinstance(inputU_tuple, tuple) and (len(inputU_tuple) == temp_flitBitWidth))

        # If the current forwarding task is on processing - Continue the current task
        if self.getStates_ifRegsLocked() is True:
            currentInPorts_tuple = self.getStates_inPortsStates()
            currentOutPorts_tuple = self.getStates_outPortsStates()
            currentFwMode = self.getStates_currentFwMode()
            assert currentFwMode in ("Fw", "NCFw")


        # If the no task is on processing - Process responses according to the Arbiter alg.
        elif self.getStates_ifRegsLocked() is False:
            # Reqs analyse
            ## IP
            if inputReqs_tuple[0] is True:
                IP_addrA_tuple = copy.deepcopy(
                    self._SimuConfig_instance.flitAnalyse_getAddrA(flit_tuple=copy.deepcopy(inputIP_tuple)))
                IP_addrB_tuple = copy.deepcopy(
                    self._SimuConfig_instance.flitAnalyse_getAddrB(flit_tuple=copy.deepcopy(inputIP_tuple)))
                IP_flitType = copy.deepcopy(
                    self._SimuConfig_instance.flitAnalyse_getType(flit_tuple=copy.deepcopy(inputIP_tuple)))

                if IP_flitType == "head":
                    reqIP_tuple = (True,
                                   IP_addrA_tuple[0], IP_addrA_tuple[1], IP_addrA_tuple[2],
                                   IP_addrB_tuple[0], IP_addrB_tuple[1], IP_addrB_tuple[2],
                                   False)
                elif IP_flitType == "NChead":
                    reqIP_tuple = (True,
                                   IP_addrA_tuple[0], IP_addrA_tuple[1], IP_addrA_tuple[2],
                                   IP_addrB_tuple[0], IP_addrB_tuple[1], IP_addrB_tuple[2],
                                   True)

            elif inputReqs_tuple[0] is False:
                reqIP_tuple = (False, 0, 0, 0, 0, 0, 0, False)
            else:
                assert False

            ## W
            if inputReqs_tuple[1] is True:
                W_addrA_tuple = copy.deepcopy(
                    self._SimuConfig_instance.flitAnalyse_getAddrA(flit_tuple=copy.deepcopy(inputW_tuple)))
                W_addrB_tuple = copy.deepcopy(
                    self._SimuConfig_instance.flitAnalyse_getAddrB(flit_tuple=copy.deepcopy(inputW_tuple)))
                W_flitType = copy.deepcopy(
                    self._SimuConfig_instance.flitAnalyse_getType(flit_tuple=copy.deepcopy(inputW_tuple)))

                if W_flitType == "head":
                    reqW_tuple = (True,
                                   W_addrA_tuple[0], W_addrA_tuple[1], W_addrA_tuple[2],
                                   W_addrB_tuple[0], W_addrB_tuple[1], W_addrB_tuple[2],
                                   False)
                elif W_flitType == "NChead":
                    reqW_tuple = (True,
                                   W_addrA_tuple[0], W_addrA_tuple[1], W_addrA_tuple[2],
                                   W_addrB_tuple[0], W_addrB_tuple[1], W_addrB_tuple[2],
                                   True)

            elif inputReqs_tuple[1] is False:
                reqW_tuple = (False, 0, 0, 0, 0, 0, 0, False)
            else:
                assert False

            ## E
            if inputReqs_tuple[2] is True:
                E_addrA_tuple = copy.deepcopy(
                    self._SimuConfig_instance.flitAnalyse_getAddrA(flit_tuple=copy.deepcopy(inputE_tuple)))
                E_addrB_tuple = copy.deepcopy(
                    self._SimuConfig_instance.flitAnalyse_getAddrB(flit_tuple=copy.deepcopy(inputE_tuple)))
                E_flitType = copy.deepcopy(
                    self._SimuConfig_instance.flitAnalyse_getType(flit_tuple=copy.deepcopy(inputE_tuple)))

                if E_flitType == "head":
                    reqE_tuple = (True,
                                   E_addrA_tuple[0], E_addrA_tuple[1], E_addrA_tuple[2],
                                   E_addrB_tuple[0], E_addrB_tuple[1], E_addrB_tuple[2],
                                   False)
                elif E_flitType == "NChead":
                    reqE_tuple = (True,
                                   E_addrA_tuple[0], E_addrA_tuple[1], E_addrA_tuple[2],
                                   E_addrB_tuple[0], E_addrB_tuple[1], E_addrB_tuple[2],
                                   True)

            elif inputReqs_tuple[2] is False:
                reqE_tuple = (False, 0, 0, 0, 0, 0, 0, False)
            else:
                assert False

            ## S
            if inputReqs_tuple[3] is True:
                S_addrA_tuple = copy.deepcopy(
                    self._SimuConfig_instance.flitAnalyse_getAddrA(flit_tuple=copy.deepcopy(inputS_tuple)))
                S_addrB_tuple = copy.deepcopy(
                    self._SimuConfig_instance.flitAnalyse_getAddrB(flit_tuple=copy.deepcopy(inputS_tuple)))
                S_flitType = copy.deepcopy(
                    self._SimuConfig_instance.flitAnalyse_getType(flit_tuple=copy.deepcopy(inputS_tuple)))

                if S_flitType == "head":
                    reqS_tuple = (True,
                                   S_addrA_tuple[0], S_addrA_tuple[1], S_addrA_tuple[2],
                                   S_addrB_tuple[0], S_addrB_tuple[1], S_addrB_tuple[2],
                                   False)
                elif S_flitType == "NChead":
                    reqS_tuple = (True,
                                   S_addrA_tuple[0], S_addrA_tuple[1], S_addrA_tuple[2],
                                   S_addrB_tuple[0], S_addrB_tuple[1], S_addrB_tuple[2],
                                   True)

            elif inputReqs_tuple[3] is False:
                reqS_tuple = (False, 0, 0, 0, 0, 0, 0, False)
            else:
                assert False

            ## N
            if inputReqs_tuple[4] is True:
                N_addrA_tuple = copy.deepcopy(
                    self._SimuConfig_instance.flitAnalyse_getAddrA(flit_tuple=copy.deepcopy(inputN_tuple)))
                N_addrB_tuple = copy.deepcopy(
                    self._SimuConfig_instance.flitAnalyse_getAddrB(flit_tuple=copy.deepcopy(inputN_tuple)))
                N_flitType = copy.deepcopy(
                    self._SimuConfig_instance.flitAnalyse_getType(flit_tuple=copy.deepcopy(inputN_tuple)))

                if N_flitType == "head":
                    reqN_tuple = (True,
                                   N_addrA_tuple[0], N_addrA_tuple[1], N_addrA_tuple[2],
                                   N_addrB_tuple[0], N_addrB_tuple[1], N_addrB_tuple[2],
                                   False)
                elif N_flitType == "NChead":
                    reqN_tuple = (True,
                                   N_addrA_tuple[0], N_addrA_tuple[1], N_addrA_tuple[2],
                                   N_addrB_tuple[0], N_addrB_tuple[1], N_addrB_tuple[2],
                                   True)

            elif inputReqs_tuple[4] is False:
                reqN_tuple = (False, 0, 0, 0, 0, 0, 0, False)
            else:
                assert False

            ## D
            if inputReqs_tuple[5] is True:
                D_addrA_tuple = copy.deepcopy(
                    self._SimuConfig_instance.flitAnalyse_getAddrA(flit_tuple=copy.deepcopy(inputD_tuple)))
                D_addrB_tuple = copy.deepcopy(
                    self._SimuConfig_instance.flitAnalyse_getAddrB(flit_tuple=copy.deepcopy(inputD_tuple)))
                D_flitType = copy.deepcopy(
                    self._SimuConfig_instance.flitAnalyse_getType(flit_tuple=copy.deepcopy(inputD_tuple)))

                if D_flitType == "head":
                    reqD_tuple = (True,
                                   D_addrA_tuple[0], D_addrA_tuple[1], D_addrA_tuple[2],
                                   D_addrB_tuple[0], D_addrB_tuple[1], D_addrB_tuple[2],
                                   False)
                elif D_flitType == "NChead":
                    reqD_tuple = (True,
                                   D_addrA_tuple[0], D_addrA_tuple[1], D_addrA_tuple[2],
                                   D_addrB_tuple[0], D_addrB_tuple[1], D_addrB_tuple[2],
                                   True)

            elif inputReqs_tuple[5] is False:
                reqD_tuple = (False, 0, 0, 0, 0, 0, 0, False)
            else:
                assert False

            ## U
            if inputReqs_tuple[6] is True:
                U_addrA_tuple = copy.deepcopy(
                    self._SimuConfig_instance.flitAnalyse_getAddrA(flit_tuple=copy.deepcopy(inputU_tuple)))
                U_addrB_tuple = copy.deepcopy(
                    self._SimuConfig_instance.flitAnalyse_getAddrB(flit_tuple=copy.deepcopy(inputU_tuple)))
                U_flitType = copy.deepcopy(
                    self._SimuConfig_instance.flitAnalyse_getType(flit_tuple=copy.deepcopy(inputU_tuple)))

                if U_flitType == "head":
                    reqU_tuple = (True,
                                   U_addrA_tuple[0], U_addrA_tuple[1], U_addrA_tuple[2],
                                   U_addrB_tuple[0], U_addrB_tuple[1], U_addrB_tuple[2],
                                   False)
                elif U_flitType == "NChead":
                    reqU_tuple = (True,
                                   U_addrA_tuple[0], U_addrA_tuple[1], U_addrA_tuple[2],
                                   U_addrB_tuple[0], U_addrB_tuple[1], U_addrB_tuple[2],
                                   True)

            elif inputReqs_tuple[6] is False:
                reqU_tuple = (False, 0, 0, 0, 0, 0, 0, False)
            else:
                assert False

            # Arbiter
            currentInPorts_tuple, currentOutPorts_tuple, currentIfPerformEncoding = imported_NCFixedPriorityArbiter.arbiterNCLogic_fixedPriority(addrLocal_tuple=self.getStates_localAddr(),
                                                                                                                                                 fifoStates_tuple=copy.deepcopy(fifoStates_tuple),
                                                                                                                                                 reqIP_tuple=copy.deepcopy(reqIP_tuple),
                                                                                                                                                 reqW_tuple=copy.deepcopy(reqW_tuple),
                                                                                                                                                 reqE_tuple=copy.deepcopy(reqE_tuple),
                                                                                                                                                 reqS_tuple=copy.deepcopy(reqS_tuple),
                                                                                                                                                 reqN_tuple=copy.deepcopy(reqN_tuple),
                                                                                                                                                 reqD_tuple=copy.deepcopy(reqD_tuple),
                                                                                                                                                 reqU_tuple=copy.deepcopy(reqU_tuple))
            if currentIfPerformEncoding is True:
                currentFwMode = "NCFw"
            elif currentIfPerformEncoding is False:
                currentFwMode = "Fw"
            else:
                assert False

        else:
            assert False

        # Forwarding####################################################################################################
        switch_flitIn_list = []
        switch_flitInCount = 0
        # IP in
        if currentInPorts_tuple[0] is True:
            switch_flitIn_list.append(copy.deepcopy(inputIP_tuple))
            switch_flitInCount = switch_flitInCount + 1
            assert inputReqs_tuple[0] is True

        # W in
        if currentInPorts_tuple[1] is True:
            switch_flitIn_list.append(copy.deepcopy(inputW_tuple))
            switch_flitInCount = switch_flitInCount + 1
            assert inputReqs_tuple[1] is True

        # E in
        if currentInPorts_tuple[2] is True:
            switch_flitIn_list.append(copy.deepcopy(inputE_tuple))
            switch_flitInCount = switch_flitInCount + 1
            assert inputReqs_tuple[2] is True

        # S in
        if currentInPorts_tuple[3] is True:
            switch_flitIn_list.append(copy.deepcopy(inputS_tuple))
            switch_flitInCount = switch_flitInCount + 1
            assert inputReqs_tuple[3] is True

        # N in
        if currentInPorts_tuple[4] is True:
            switch_flitIn_list.append(copy.deepcopy(inputN_tuple))
            switch_flitInCount = switch_flitInCount + 1
            assert inputReqs_tuple[4] is True

        # D in
        if currentInPorts_tuple[5] is True:
            switch_flitIn_list.append(copy.deepcopy(inputD_tuple))
            switch_flitInCount = switch_flitInCount + 1
            assert inputReqs_tuple[5] is True

        # U in
        if currentInPorts_tuple[6] is True:
            switch_flitIn_list.append(copy.deepcopy(inputU_tuple))
            switch_flitInCount = switch_flitInCount + 1
            assert inputReqs_tuple[6] is True

        assert len(switch_flitIn_list) == switch_flitInCount
        assert switch_flitInCount in (0, 1, 2)

        # Mode 1: Forward an Uncoded/Encoded packet
        if switch_flitInCount == 1:
            switch_flitIn = copy.deepcopy(switch_flitIn_list[1])
            switch_flitOutCount = 0

            # IP out
            if currentOutPorts_tuple[0] is True:
                outIP_tuple = copy.deepcopy(switch_flitIn)
                switch_flitOutCount = switch_flitOutCount + 1
                assert fifoStates_tuple[0] is True
            elif currentOutPorts_tuple[0] is False:
                outIP_tuple = None
            else:
                assert False

            # W out
            if currentOutPorts_tuple[1] is True:
                outW_tuple = copy.deepcopy(switch_flitIn)
                switch_flitOutCount = switch_flitOutCount + 1
                assert fifoStates_tuple[1] is True
            elif currentOutPorts_tuple[1] is False:
                outW_tuple = None
            else:
                assert False

            # E out
            if currentOutPorts_tuple[2] is True:
                outE_tuple = copy.deepcopy(switch_flitIn)
                switch_flitOutCount = switch_flitOutCount + 1
                assert fifoStates_tuple[2] is True
            elif currentOutPorts_tuple[2] is False:
                outE_tuple = None
            else:
                assert False

            # S out
            if currentOutPorts_tuple[3] is True:
                outS_tuple = copy.deepcopy(switch_flitIn)
                switch_flitOutCount = switch_flitOutCount + 1
                assert fifoStates_tuple[3] is True
            elif currentOutPorts_tuple[3] is False:
                outS_tuple = None
            else:
                assert False

            # N out
            if currentOutPorts_tuple[4] is True:
                outN_tuple = copy.deepcopy(switch_flitIn)
                switch_flitOutCount = switch_flitOutCount + 1
                assert fifoStates_tuple[4] is True
            elif currentOutPorts_tuple[4] is False:
                outN_tuple = None
            else:
                assert False

            # D out
            if currentOutPorts_tuple[5] is True:
                outD_tuple = copy.deepcopy(switch_flitIn)
                switch_flitOutCount = switch_flitOutCount + 1
                assert fifoStates_tuple[5] is True
            elif currentOutPorts_tuple[5] is False:
                outD_tuple = None
            else:
                assert False

            # U out
            if currentOutPorts_tuple[6] is True:
                outU_tuple = copy.deepcopy(switch_flitIn)
                switch_flitOutCount = switch_flitOutCount + 1
                assert fifoStates_tuple[6] is True
            elif currentOutPorts_tuple[6] is False:
                outU_tuple = None
            else:
                assert False

            # Post process
            if self.getStates_ifRegsLocked() is True:
                assert switch_flitOutCount in (1, 2)
                assert switch_flitInCount == 1

                # Update the router states (regs) according to the flit processed.
                switch_flitIn_flitType = self._SimuConfig_instance.flitAnalyse_getType(flit_tuple=copy.deepcopy(switch_flitIn))
                assert switch_flitIn_flitType in ("payload", "tail")
                if switch_flitIn_flitType == "tail":
                    self.resetStates()

            elif self.getStates_ifRegsLocked() is False:
                assert switch_flitOutCount in (0, 1, 2)
                assert switch_flitInCount in (0, 1)

                # Update the router states (regs) according to the flit processed.
                if switch_flitInCount == 1:
                    switch_flitIn_flitType = self._SimuConfig_instance.flitAnalyse_getType(flit_tuple=copy.deepcopy(switch_flitIn))
                    # assert switch_flitIn_flitType in ("head", "NChead")
                    if switch_flitIn_flitType == "head":
                        assert switch_flitOutCount == 1
                        assert currentFwMode == "Fw"
                        self.updateStates_lock(inPorts_tuple=copy.deepcopy(currentInPorts_tuple), outPorts_tuple=copy.deepcopy(currentOutPorts_tuple), newFwMode=copy.deepcopy(currentFwMode))
                    elif switch_flitIn_flitType == "NChead":
                        assert currentFwMode == "Fw"
                        self.updateStates_lock(inPorts_tuple=copy.deepcopy(currentInPorts_tuple), outPorts_tuple=copy.deepcopy(currentOutPorts_tuple), newFwMode=copy.deepcopy(currentFwMode))
                    else:
                        assert False

        # Mode 2: Encoding and Forwarding
        elif switch_flitInCount == 2:
            # Encoding
            switch_flitIn_A = copy.deepcopy(switch_flitIn_list[0])
            switch_flitIn_B = copy.deepcopy(switch_flitIn_list[1])
            temp_flitBitWidth = self.getConfig_flitBitWidth()
            assert len(switch_flitIn_A) == temp_flitBitWidth
            assert len(switch_flitIn_B) == temp_flitBitWidth

            switch_flitIn_flitType = self._SimuConfig_instance.flitAnalyse_getType(flit_tuple=copy.deepcopy(switch_flitIn_A))
            assert self._SimuConfig_instance.flitAnalyse_getType(flit_tuple=copy.deepcopy(switch_flitIn_B)) == switch_flitIn_flitType
            assert switch_flitIn_flitType in ("head", "payload", "tail")

            ## Encoding head flits
            if switch_flitIn_flitType == "head":
                switch_flitIn = copy.deepcopy(self.XORNC_encodingHeadFlits(flit_A=copy.deepcopy(switch_flitIn_A), flit_B=copy.deepcopy(switch_flitIn_B)))
            ## Encoding payloads
            elif switch_flitIn_flitType == "payload":
                switch_encodedFlit_list = []
                switch_encodedFlit_list.append(False)
                for idx_i in range(1, temp_flitBitWidth):
                    assert switch_flitIn_A[idx_i] in (True, False)
                    assert switch_flitIn_B[idx_i] in (True, False)
                    if switch_flitIn_A[idx_i] == switch_flitIn_B[idx_i]:
                        switch_encodedFlit_list.append(False)
                    else:
                        switch_encodedFlit_list.append(True)
                switch_flitIn = tuple(switch_encodedFlit_list)

            ## Encoding tail flits
            elif switch_flitIn_flitType == "tail":
                switch_flitIn = copy.deepcopy(switch_flitIn_A)

            else:
                assert False


            switch_flitOutCount = 0

            # IP out
            if currentOutPorts_tuple[0] is True:
                outIP_tuple = copy.deepcopy(switch_flitIn)
                switch_flitOutCount = switch_flitOutCount + 1
                assert fifoStates_tuple[0] is True
            elif currentOutPorts_tuple[0] is False:
                outIP_tuple = None
            else:
                assert False

            # W out
            if currentOutPorts_tuple[1] is True:
                outW_tuple = copy.deepcopy(switch_flitIn)
                switch_flitOutCount = switch_flitOutCount + 1
                assert fifoStates_tuple[1] is True
            elif currentOutPorts_tuple[1] is False:
                outW_tuple = None
            else:
                assert False

            # E out
            if currentOutPorts_tuple[2] is True:
                outE_tuple = copy.deepcopy(switch_flitIn)
                switch_flitOutCount = switch_flitOutCount + 1
                assert fifoStates_tuple[2] is True
            elif currentOutPorts_tuple[2] is False:
                outE_tuple = None
            else:
                assert False

            # S out
            if currentOutPorts_tuple[3] is True:
                outS_tuple = copy.deepcopy(switch_flitIn)
                switch_flitOutCount = switch_flitOutCount + 1
                assert fifoStates_tuple[3] is True
            elif currentOutPorts_tuple[3] is False:
                outS_tuple = None
            else:
                assert False

            # N out
            if currentOutPorts_tuple[4] is True:
                outN_tuple = copy.deepcopy(switch_flitIn)
                switch_flitOutCount = switch_flitOutCount + 1
                assert fifoStates_tuple[4] is True
            elif currentOutPorts_tuple[4] is False:
                outN_tuple = None
            else:
                assert False

            # D out
            if currentOutPorts_tuple[5] is True:
                outD_tuple = copy.deepcopy(switch_flitIn)
                switch_flitOutCount = switch_flitOutCount + 1
                assert fifoStates_tuple[5] is True
            elif currentOutPorts_tuple[5] is False:
                outD_tuple = None
            else:
                assert False

            # U out
            if currentOutPorts_tuple[6] is True:
                outU_tuple = copy.deepcopy(switch_flitIn)
                switch_flitOutCount = switch_flitOutCount + 1
                assert fifoStates_tuple[6] is True
            elif currentOutPorts_tuple[6] is False:
                outU_tuple = None
            else:
                assert False

            # Post process
            if self.getStates_ifRegsLocked() is True:
                assert switch_flitOutCount in (1, 2)
                assert switch_flitInCount == 2
                assert currentFwMode == "NCFw"

                # Update the router states (regs) according to the flit processed.
                if switch_flitIn_flitType == "tail":
                    self.resetStates()
                else:
                    assert switch_flitIn_flitType == "payload"

            elif self.getStates_ifRegsLocked() is False:
                assert switch_flitOutCount in (1, 2)
                assert switch_flitInCount == 2
                assert currentFwMode == "NCFw"

                # Update the router states (regs) according to the flit processed.
                assert switch_flitIn_flitType == "head"
                self.updateStates_lock(inPorts_tuple=copy.deepcopy(currentInPorts_tuple), outPorts_tuple=copy.deepcopy(currentOutPorts_tuple), newFwMode=copy.deepcopy(currentFwMode))


        # Return
        return copy.deepcopy(currentInPorts_tuple), copy.deepcopy(currentOutPorts_tuple), copy.deepcopy(outIP_tuple), copy.deepcopy(outW_tuple), copy.deepcopy(outE_tuple), copy.deepcopy(outS_tuple), copy.deepcopy(outN_tuple), copy.deepcopy(outD_tuple), copy.deepcopy(outU_tuple)


########################################################################################################################
########################################################################################################################