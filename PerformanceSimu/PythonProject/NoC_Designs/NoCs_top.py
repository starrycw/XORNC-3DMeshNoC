import copy

import NoC_Designs.Routers_top as imported_Routers_top
import NoC_Designs.FIFOs_top as imported_FIFOs_top
import Simulation.SimuConfigurationClass as imported_ActiveConfiguration


########################################################################################################################
########################################################################################################################
class Router_FIFO_FP_top:
    '''
    The router with output FIFOs.
    '''
    def __init__(self, router_id, routerAddr_tuple, SimuConfig_instance):
        # assert isinstance(SimuConfig_instance, imported_ActiveConfiguration.SimuConfigs)
        self._param_router_id = copy.deepcopy(router_id)
        self._param_routerAddr_tuple = copy.deepcopy(routerAddr_tuple)
        self._param_SimuConfig = SimuConfig_instance

        self.reset_all()

        # self._mainRouterInstance = imported_Routers_top.RoutersTop_FP(router_id=copy.deepcopy(router_id), routerAddr_tuple=copy.deepcopy(routerAddr_tuple), SimuConfig_instance=SimuConfig_instance)
        #
        # self._mainFIFOInstance_outIP = imported_FIFOs_top.FIFOsTop(
        #     flit_depth=SimuConfig_instance.getParam_FIFOFlitDepth(),
        #     flit_bw=SimuConfig_instance.getParam_flitBitWidth(), fifo_id=0)
        #
        # self._mainFIFOInstance_outW = imported_FIFOs_top.FIFOsTop(
        #     flit_depth=SimuConfig_instance.getParam_FIFOFlitDepth(),
        #     flit_bw=SimuConfig_instance.getParam_flitBitWidth(), fifo_id=1)
        #
        # self._mainFIFOInstance_outE = imported_FIFOs_top.FIFOsTop(
        #     flit_depth=SimuConfig_instance.getParam_FIFOFlitDepth(),
        #     flit_bw=SimuConfig_instance.getParam_flitBitWidth(), fifo_id=2)
        #
        # self._mainFIFOInstance_outS = imported_FIFOs_top.FIFOsTop(
        #     flit_depth=SimuConfig_instance.getParam_FIFOFlitDepth(),
        #     flit_bw=SimuConfig_instance.getParam_flitBitWidth(), fifo_id=3)
        #
        # self._mainFIFOInstance_outN = imported_FIFOs_top.FIFOsTop(
        #     flit_depth=SimuConfig_instance.getParam_FIFOFlitDepth(),
        #     flit_bw=SimuConfig_instance.getParam_flitBitWidth(), fifo_id=4)
        #
        # self._mainFIFOInstance_outD = imported_FIFOs_top.FIFOsTop(
        #     flit_depth=SimuConfig_instance.getParam_FIFOFlitDepth(),
        #     flit_bw=SimuConfig_instance.getParam_flitBitWidth(), fifo_id=5)
        #
        # self._mainFIFOInstance_outU = imported_FIFOs_top.FIFOsTop(
        #     flit_depth=SimuConfig_instance.getParam_FIFOFlitDepth(),
        #     flit_bw=SimuConfig_instance.getParam_flitBitWidth(), fifo_id=6)
        #
        # self._mainFIFOInstance_inIP = imported_FIFOs_top.FIFOsTop(
        #     flit_depth=SimuConfig_instance.getParam_IPFlitSent_nMax(),
        #     flit_bw=SimuConfig_instance.getParam_flitBitWidth(), fifo_id=10)
    ####################################################################################################################
    def reset_all(self):
        self._mainRouterInstance = imported_Routers_top.RoutersTop_FP(router_id=copy.deepcopy(self._param_router_id),
                                                                      routerAddr_tuple=copy.deepcopy(self._param_routerAddr_tuple),
                                                                      SimuConfig_instance=self._param_SimuConfig)

        self._mainFIFOInstance_outIP = imported_FIFOs_top.FIFOsTop(
            flit_depth=self._param_SimuConfig.getParam_IPFlitReceive_nMax(),
            flit_bw=self._param_SimuConfig.getParam_flitBitWidth(), fifo_id=0)

        self._mainFIFOInstance_outW = imported_FIFOs_top.FIFOsTop(
            flit_depth=self._param_SimuConfig.getParam_FIFOFlitDepth(),
            flit_bw=self._param_SimuConfig.getParam_flitBitWidth(), fifo_id=1)

        self._mainFIFOInstance_outE = imported_FIFOs_top.FIFOsTop(
            flit_depth=self._param_SimuConfig.getParam_FIFOFlitDepth(),
            flit_bw=self._param_SimuConfig.getParam_flitBitWidth(), fifo_id=2)

        self._mainFIFOInstance_outS = imported_FIFOs_top.FIFOsTop(
            flit_depth=self._param_SimuConfig.getParam_FIFOFlitDepth(),
            flit_bw=self._param_SimuConfig.getParam_flitBitWidth(), fifo_id=3)

        self._mainFIFOInstance_outN = imported_FIFOs_top.FIFOsTop(
            flit_depth=self._param_SimuConfig.getParam_FIFOFlitDepth(),
            flit_bw=self._param_SimuConfig.getParam_flitBitWidth(), fifo_id=4)

        self._mainFIFOInstance_outD = imported_FIFOs_top.FIFOsTop(
            flit_depth=self._param_SimuConfig.getParam_FIFOFlitDepth(),
            flit_bw=self._param_SimuConfig.getParam_flitBitWidth(), fifo_id=5)

        self._mainFIFOInstance_outU = imported_FIFOs_top.FIFOsTop(
            flit_depth=self._param_SimuConfig.getParam_FIFOFlitDepth(),
            flit_bw=self._param_SimuConfig.getParam_flitBitWidth(), fifo_id=6)

        self._mainFIFOInstance_inIP = imported_FIFOs_top.FIFOsTop(
            flit_depth=self._param_SimuConfig.getParam_IPFlitSent_nMax(),
            flit_bw=self._param_SimuConfig.getParam_flitBitWidth(), fifo_id=10)




    ####################################################################################################################
    def getParam_address(self):
        return copy.deepcopy(self._param_routerAddr_tuple)
    ####################################################################################################################
    def getRouterStates(self):
        '''
        Get the states of Router module
        :return: bool(If locked), str(FW mode), tuple(If input ports enabled), tuple(If output ports enabled)
        '''
        rState_ifLocked = self._mainRouterInstance.getStates_ifRegsLocked()
        rState_currentFwMode = self._mainRouterInstance.getStates_currentFwMode()
        rState_currentEnabledInPort = self._mainRouterInstance.getStates_inPortsStates()
        rState_currentEnabledOutPort = self._mainRouterInstance.getStates_outPortsStates()
        return copy.deepcopy(rState_ifLocked), copy.deepcopy(rState_currentFwMode), copy.deepcopy(rState_currentEnabledInPort), copy.deepcopy(rState_currentEnabledOutPort)
    ####################################################################################################################
    def router_updateNextCycle_Step1(self, inputReqs_tuple,
                     inputIP_tuple=None, inputW_tuple=None, inputE_tuple=None, inputS_tuple=None, inputN_tuple=None, inputD_tuple=None, inputU_tuple=None):

        if self._mainFIFOInstance_outIP.getState_ifFull() is True:
            FIFO_IP_state = False
        elif self._mainFIFOInstance_outIP.getState_ifFull() is False:
            FIFO_IP_state = True
        else:
            assert False

        if self._mainFIFOInstance_outW.getState_ifFull() is True:
            FIFO_W_state = False
        elif self._mainFIFOInstance_outW.getState_ifFull() is False:
            FIFO_W_state = True
        else:
            assert False

        if self._mainFIFOInstance_outE.getState_ifFull() is True:
            FIFO_E_state = False
        elif self._mainFIFOInstance_outE.getState_ifFull() is False:
            FIFO_E_state = True
        else:
            assert False

        if self._mainFIFOInstance_outS.getState_ifFull() is True:
            FIFO_S_state = False
        elif self._mainFIFOInstance_outS.getState_ifFull() is False:
            FIFO_S_state = True
        else:
            assert False

        if self._mainFIFOInstance_outN.getState_ifFull() is True:
            FIFO_N_state = False
        elif self._mainFIFOInstance_outN.getState_ifFull() is False:
            FIFO_N_state = True
        else:
            assert False

        if self._mainFIFOInstance_outD.getState_ifFull() is True:
            FIFO_D_state = False
        elif self._mainFIFOInstance_outD.getState_ifFull() is False:
            FIFO_D_state = True
        else:
            assert False

        if self._mainFIFOInstance_outU.getState_ifFull() is True:
            FIFO_U_state = False
        elif self._mainFIFOInstance_outU.getState_ifFull() is False:
            FIFO_U_state = True
        else:
            assert False

        FIFO_all_states = (FIFO_IP_state, FIFO_W_state, FIFO_E_state, FIFO_S_state, FIFO_N_state, FIFO_D_state, FIFO_U_state)

        activeIn_tuple, activeOut_tuple, outIP_tuple, outW_tuple, outE_tuple, outS_tuple, outN_tuple, outD_tuple, outU_tuple = self._mainRouterInstance.run_nextCycle(
            fifoStates_tuple=copy.deepcopy(FIFO_all_states), inputReqs_tuple=inputReqs_tuple,
            inputIP_tuple=inputIP_tuple, inputW_tuple=inputW_tuple, inputE_tuple=inputE_tuple,
            inputS_tuple=inputS_tuple, inputN_tuple=inputN_tuple, inputD_tuple=inputD_tuple, inputU_tuple=inputU_tuple)

        self._tempFIFOInstance_outIP = copy.deepcopy(self._mainFIFOInstance_outIP)
        self._tempFIFOInstance_outW = copy.deepcopy(self._mainFIFOInstance_outW)
        self._tempFIFOInstance_outE = copy.deepcopy(self._mainFIFOInstance_outE)
        self._tempFIFOInstance_outS = copy.deepcopy(self._mainFIFOInstance_outS)
        self._tempFIFOInstance_outN = copy.deepcopy(self._mainFIFOInstance_outN)
        self._tempFIFOInstance_outD = copy.deepcopy(self._mainFIFOInstance_outD)
        self._tempFIFOInstance_outU = copy.deepcopy(self._mainFIFOInstance_outU)
        if activeOut_tuple[0] is True:
            self._tempFIFOInstance_outIP.memOp_writeOneFlit(flitNew=copy.deepcopy(outIP_tuple))
        else:
            assert activeOut_tuple[0] is False

        if activeOut_tuple[1] is True:
            self._tempFIFOInstance_outW.memOp_writeOneFlit(flitNew=copy.deepcopy(outW_tuple))
        else:
            assert activeOut_tuple[1] is False

        if activeOut_tuple[2] is True:
            self._tempFIFOInstance_outE.memOp_writeOneFlit(flitNew=copy.deepcopy(outE_tuple))
        else:
            assert activeOut_tuple[2] is False

        if activeOut_tuple[3] is True:
            self._tempFIFOInstance_outS.memOp_writeOneFlit(flitNew=copy.deepcopy(outS_tuple))
        else:
            assert activeOut_tuple[3] is False

        if activeOut_tuple[4] is True:
            self._tempFIFOInstance_outN.memOp_writeOneFlit(flitNew=copy.deepcopy(outN_tuple))
        else:
            assert activeOut_tuple[4] is False

        if activeOut_tuple[5] is True:
            self._tempFIFOInstance_outD.memOp_writeOneFlit(flitNew=copy.deepcopy(outD_tuple))
        else:
            assert activeOut_tuple[5] is False

        if activeOut_tuple[6] is True:
            self._tempFIFOInstance_outU.memOp_writeOneFlit(flitNew=copy.deepcopy(outU_tuple))
        else:
            assert activeOut_tuple[6] is False

        return copy.deepcopy(activeIn_tuple)

    def router_updateNextCycle_Step2(self):
        self._mainFIFOInstance_outIP = copy.deepcopy(self._tempFIFOInstance_outIP)
        self._mainFIFOInstance_outW = copy.deepcopy(self._tempFIFOInstance_outW)
        self._mainFIFOInstance_outE = copy.deepcopy(self._tempFIFOInstance_outE)
        self._mainFIFOInstance_outS = copy.deepcopy(self._tempFIFOInstance_outS)
        self._mainFIFOInstance_outN = copy.deepcopy(self._tempFIFOInstance_outN)
        self._mainFIFOInstance_outD = copy.deepcopy(self._tempFIFOInstance_outD)
        self._mainFIFOInstance_outU = copy.deepcopy(self._tempFIFOInstance_outU)

    ####################################################################################################################
    def FIFO_getFirstFlit_byPortName(self, portName):
        '''

        :param portName: in ("IP", "W", "E", "S", "N", "D", "U")
        :return: tuple
        '''
        if portName == "IP":
            return copy.deepcopy(self._mainFIFOInstance_outIP.memOp_getFirstFlit())
        elif portName == "W":
            return copy.deepcopy(self._mainFIFOInstance_outW.memOp_getFirstFlit())
        elif portName == "E":
            return copy.deepcopy(self._mainFIFOInstance_outE.memOp_getFirstFlit())
        elif portName == "S":
            return copy.deepcopy(self._mainFIFOInstance_outS.memOp_getFirstFlit())
        elif portName == "N":
            return copy.deepcopy(self._mainFIFOInstance_outN.memOp_getFirstFlit())
        elif portName == "D":
            return copy.deepcopy(self._mainFIFOInstance_outD.memOp_getFirstFlit())
        elif portName == "U":
            return copy.deepcopy(self._mainFIFOInstance_outU.memOp_getFirstFlit())
        else:
            assert False
    ####################################################################################################################
    def FIFO_deleteOneFlit_byPortName(self, portName):
        '''

        :param portName: in ("IP", "W", "E", "S", "N", "D", "U")
        :return:
        '''
        if portName == "IP":
            self._mainFIFOInstance_outIP.memOp_deleteFirstFlit()
            self._tempFIFOInstance_outIP.memOp_deleteFirstFlit()
        elif portName == "W":
            self._mainFIFOInstance_outW.memOp_deleteFirstFlit()
            self._tempFIFOInstance_outW.memOp_deleteFirstFlit()
        elif portName == "E":
            self._mainFIFOInstance_outE.memOp_deleteFirstFlit()
            self._tempFIFOInstance_outE.memOp_deleteFirstFlit()
        elif portName == "S":
            self._mainFIFOInstance_outS.memOp_deleteFirstFlit()
            self._tempFIFOInstance_outS.memOp_deleteFirstFlit()
        elif portName == "N":
            self._mainFIFOInstance_outN.memOp_deleteFirstFlit()
            self._tempFIFOInstance_outN.memOp_deleteFirstFlit()
        elif portName == "D":
            self._mainFIFOInstance_outD.memOp_deleteFirstFlit()
            self._tempFIFOInstance_outD.memOp_deleteFirstFlit()
        elif portName == "U":
            self._mainFIFOInstance_outU.memOp_deleteFirstFlit()
            self._tempFIFOInstance_outU.memOp_deleteFirstFlit()
        else:
            assert False

    ####################################################################################################################
    def FIFO_checkIfEmpty_byPortName(self, portName):
        '''
        Check if the selected FIFO is empty
        :param portName: in ("IP", "W", "E", "S", "N", "D", "U")
        :return: bool
        '''
        if portName == "IP":
            return copy.deepcopy(self._mainFIFOInstance_outIP.getState_ifEmpty())
        elif portName == "W":
            return copy.deepcopy(self._mainFIFOInstance_outW.getState_ifEmpty())
        elif portName == "E":
            return copy.deepcopy(self._mainFIFOInstance_outE.getState_ifEmpty())
        elif portName == "S":
            return copy.deepcopy(self._mainFIFOInstance_outS.getState_ifEmpty())
        elif portName == "N":
            return copy.deepcopy(self._mainFIFOInstance_outN.getState_ifEmpty())
        elif portName == "D":
            return copy.deepcopy(self._mainFIFOInstance_outD.getState_ifEmpty())
        elif portName == "U":
            return copy.deepcopy(self._mainFIFOInstance_outU.getState_ifEmpty())
        else:
            assert False

    ####################################################################################################################
    def FIFOIPIn_injectFlit(self, flitInjected):
        assert isinstance(flitInjected, tuple) and (len(flitInjected) == self._param_SimuConfig.getParam_flitBitWidth())
        self._mainFIFOInstance_inIP.memOp_writeOneFlit(flitNew=copy.deepcopy(flitInjected))
    ####################################################################################################################
    def FIFOIPIn_checkIfEmpty(self):
        return copy.deepcopy(self._mainFIFOInstance_inIP.getState_ifEmpty())
    ####################################################################################################################
    def FIFOIPIn_getFirstFlit(self):
        return copy.deepcopy(self._mainFIFOInstance_inIP.memOp_getFirstFlit())
    ####################################################################################################################
    def FIFOIPIn_deleteOneFlit(self):
        self._mainFIFOInstance_inIP.memOp_deleteFirstFlit()

########################################################################################################################
########################################################################################################################
class Router_FIFO_NCFP_top(Router_FIFO_FP_top):
    def __init__(self, router_id, routerAddr_tuple, SimuConfig_instance):
        # assert isinstance(SimuConfig_instance, imported_ActiveConfiguration.SimuConfigs)
        self._param_router_id = copy.deepcopy(router_id)
        self._param_routerAddr_tuple = copy.deepcopy(routerAddr_tuple)
        self._param_SimuConfig = SimuConfig_instance

        self.reset_all()

    def reset_all(self):
        self._mainRouterInstance = imported_Routers_top.RoutersTop_NCFP(router_id=copy.deepcopy(self._param_router_id),
                                                                      routerAddr_tuple=copy.deepcopy(self._param_routerAddr_tuple),
                                                                      SimuConfig_instance=self._param_SimuConfig)

        self._mainFIFOInstance_outIP = imported_FIFOs_top.FIFOsTop(
            flit_depth=self._param_SimuConfig.getParam_IPFlitReceive_nMax(),
            flit_bw=self._param_SimuConfig.getParam_flitBitWidth(), fifo_id=0)

        self._mainFIFOInstance_outW = imported_FIFOs_top.FIFOsTop(
            flit_depth=self._param_SimuConfig.getParam_FIFOFlitDepth(),
            flit_bw=self._param_SimuConfig.getParam_flitBitWidth(), fifo_id=1)

        self._mainFIFOInstance_outE = imported_FIFOs_top.FIFOsTop(
            flit_depth=self._param_SimuConfig.getParam_FIFOFlitDepth(),
            flit_bw=self._param_SimuConfig.getParam_flitBitWidth(), fifo_id=2)

        self._mainFIFOInstance_outS = imported_FIFOs_top.FIFOsTop(
            flit_depth=self._param_SimuConfig.getParam_FIFOFlitDepth(),
            flit_bw=self._param_SimuConfig.getParam_flitBitWidth(), fifo_id=3)

        self._mainFIFOInstance_outN = imported_FIFOs_top.FIFOsTop(
            flit_depth=self._param_SimuConfig.getParam_FIFOFlitDepth(),
            flit_bw=self._param_SimuConfig.getParam_flitBitWidth(), fifo_id=4)

        self._mainFIFOInstance_outD = imported_FIFOs_top.FIFOsTop(
            flit_depth=self._param_SimuConfig.getParam_FIFOFlitDepth(),
            flit_bw=self._param_SimuConfig.getParam_flitBitWidth(), fifo_id=5)

        self._mainFIFOInstance_outU = imported_FIFOs_top.FIFOsTop(
            flit_depth=self._param_SimuConfig.getParam_FIFOFlitDepth(),
            flit_bw=self._param_SimuConfig.getParam_flitBitWidth(), fifo_id=6)

        self._mainFIFOInstance_inIP = imported_FIFOs_top.FIFOsTop(
            flit_depth=self._param_SimuConfig.getParam_IPFlitSent_nMax(),
            flit_bw=self._param_SimuConfig.getParam_flitBitWidth(), fifo_id=10)



########################################################################################################################
########################################################################################################################
class NoCsTop_BASE:
    def __init__(self):
        self._param_NoCSizeX = None
        self._param_NoCSizeY = None
        self._param_NoCSizeZ = None
        self._param_SimuConfigInstance = None
        assert False

    def getParam_NoCSizeX(self):
        return copy.deepcopy(self._param_NoCSizeX)

    def getParam_NoCSizeY(self):
        return copy.deepcopy(self._param_NoCSizeY)

    def getParam_NoCSizeZ(self):
        return copy.deepcopy(self._param_NoCSizeZ)

    def _NoCTopologyInit(self):
        # self._mainTopo = [ [ [None]*(self.getParam_NoCSizeZ()) ]*(self.getParam_NoCSizeY()) ]*(self.getParam_NoCSizeX())
        self._mainTopo = []
        router_id = 0
        for idx_xi in range(0, self.getParam_NoCSizeX()):
            for idx_yi in range(0, self.getParam_NoCSizeY()):
                for idx_zi in range(0, self.getParam_NoCSizeZ()):
                    assert self._mainTopo[idx_xi][idx_yi][idx_zi] is None
                    self._mainTopo[idx_xi][idx_yi][idx_zi] = Router_FIFO_FP_top(router_id=router_id,
                                                                                routerAddr_tuple=(copy.deepcopy(idx_xi),
                                                                                                  copy.deepcopy(idx_yi),
                                                                                                  copy.deepcopy(
                                                                                                      idx_zi)),
                                                                                SimuConfig_instance=self._param_SimuConfigInstance)
                    router_id = router_id + 1
        print("NoC Topology Initialization - Done!")
        assert False

    def resetNoCTopo(self):
        self._NoCTopologyInit()

    def check_boundaryFlitOverflow(self):
        '''
        For ckeck if there exists flit stored in the boundary output FIFOs incorrectly.

        This function helps to check for errors in algorithms or coding.
        :return:
        '''
        # Boundary W & E
        for idx_temp_zi in range(0, self.getParam_NoCSizeZ()):
            for idx_temp_yi in range(0, self.getParam_NoCSizeY()):
                # print(self._mainTopo[0][idx_temp_yi][idx_temp_zi].FIFO_getFirstFlit_byPortName(portName="W"))
                # print(self._mainTopo[0][idx_temp_yi][idx_temp_zi].FIFO_getFirstFlit_byPortName(portName="E"))
                assert self._mainTopo[0][idx_temp_yi][idx_temp_zi].FIFO_checkIfEmpty_byPortName(portName="W") is True
                assert self._mainTopo[-1][idx_temp_yi][idx_temp_zi].FIFO_checkIfEmpty_byPortName(portName="E") is True

        # Boundary S & N
        for idx_temp_zi in range(0, self.getParam_NoCSizeZ()):
            for idx_temp_xi in range(0, self.getParam_NoCSizeX()):
                assert self._mainTopo[idx_temp_xi][0][idx_temp_zi].FIFO_checkIfEmpty_byPortName(portName="S") is True
                assert self._mainTopo[idx_temp_xi][-1][idx_temp_zi].FIFO_checkIfEmpty_byPortName(portName="N") is True

        # Boundary D & U
        for idx_temp_yi in range(0, self.getParam_NoCSizeY()):
            for idx_temp_xi in range(0, self.getParam_NoCSizeX()):
                assert self._mainTopo[idx_temp_xi][idx_temp_yi][0].FIFO_checkIfEmpty_byPortName(portName="D") is True
                assert self._mainTopo[idx_temp_xi][idx_temp_yi][-1].FIFO_checkIfEmpty_byPortName(portName="U") is True

    def getRouterInput_byPortName(self, routerAddr, portName):
        '''
        Get the current input flit in the portName port of the router with address routerAddr.
        :param routerAddr:
        :param portName:
        :return: bool, tuple(or None) - If has req & The input flit.
        '''
        assert isinstance(routerAddr, tuple) and (len(routerAddr) == 3)
        targetAddr_X = copy.deepcopy(routerAddr[0])
        targetAddr_Y = copy.deepcopy(routerAddr[1])
        targetAddr_Z = copy.deepcopy(routerAddr[2])

        if portName == "W":
            targetAddr_X = targetAddr_X - 1
            targetPortName = "E"

        elif portName == "E":
            targetAddr_X = targetAddr_X + 1
            targetPortName = "W"

        elif portName == "S":
            targetAddr_Y = targetAddr_Y - 1
            targetPortName = "N"

        elif portName == "N":
            targetAddr_Y = targetAddr_Y + 1
            targetPortName = "S"

        elif portName == "D":
            targetAddr_Z = targetAddr_Z - 1
            targetPortName = "U"

        elif portName == "U":
            targetAddr_Z = targetAddr_Z + 1
            targetPortName = "D"

        else:
            assert portName == "IP"
            targetPortName = None

        if (targetAddr_X < 0) or (targetAddr_X >= self.getParam_NoCSizeX()):
            assert not (targetAddr_X > self.getParam_NoCSizeX())
            return False, None

        elif (targetAddr_Y < 0) or (targetAddr_Y >= self.getParam_NoCSizeY()):
            assert not (targetAddr_Y > self.getParam_NoCSizeY())
            return False, None

        elif (targetAddr_Z < 0) or (targetAddr_Z >= self.getParam_NoCSizeZ()):
            assert not (targetAddr_Z > self.getParam_NoCSizeZ())
            return False, None

        elif portName == "IP":
            if self._mainTopo[targetAddr_X][targetAddr_Y][targetAddr_Z].FIFOIPIn_checkIfEmpty() is True:
                ifHasInputReq = False
            elif self._mainTopo[targetAddr_X][targetAddr_Y][targetAddr_Z].FIFOIPIn_checkIfEmpty() is False:
                ifHasInputReq = True
            else:
                print("ERROR DATA:")
                print(self._mainTopo[targetAddr_X][targetAddr_Y][targetAddr_Z].FIFOIPIn_checkIfEmpty())
                assert False
            return copy.deepcopy(ifHasInputReq), copy.deepcopy(self._mainTopo[targetAddr_X][targetAddr_Y][targetAddr_Z].FIFOIPIn_getFirstFlit())

        else:
            if self._mainTopo[targetAddr_X][targetAddr_Y][targetAddr_Z].FIFO_checkIfEmpty_byPortName(portName=targetPortName) is True:
                ifHasInputReq = False
            elif self._mainTopo[targetAddr_X][targetAddr_Y][targetAddr_Z].FIFO_checkIfEmpty_byPortName(portName=targetPortName) is False:
                ifHasInputReq = True
            else:
                assert False
            return copy.deepcopy(ifHasInputReq), copy.deepcopy(self._mainTopo[targetAddr_X][targetAddr_Y][targetAddr_Z].FIFO_getFirstFlit_byPortName(portName=targetPortName))

    def update_inputFlitReceived(self, routerAddr, portName):
        '''
        Delete the current flit in the specified direction
        :param routerAddr:
        :param portName:
        :return:
        '''
        assert isinstance(routerAddr, tuple) and (len(routerAddr) == 3)
        targetAddr_X = copy.deepcopy(routerAddr[0])
        targetAddr_Y = copy.deepcopy(routerAddr[1])
        targetAddr_Z = copy.deepcopy(routerAddr[2])

        if portName == "W":
            targetAddr_X = targetAddr_X - 1
            targetPortName = "E"

        elif portName == "E":
            targetAddr_X = targetAddr_X + 1
            targetPortName = "W"

        elif portName == "S":
            targetAddr_Y = targetAddr_Y - 1
            targetPortName = "N"

        elif portName == "N":
            targetAddr_Y = targetAddr_Y + 1
            targetPortName = "S"

        elif portName == "D":
            targetAddr_Z = targetAddr_Z - 1
            targetPortName = "U"

        elif portName == "U":
            targetAddr_Z = targetAddr_Z + 1
            targetPortName = "D"

        else:
            assert portName == "IP"
            targetPortName = None

        if (targetAddr_X < 0) or (targetAddr_X >= self.getParam_NoCSizeX()):
            assert False

        if (targetAddr_Y < 0) or (targetAddr_Y >= self.getParam_NoCSizeY()):
            assert False

        if (targetAddr_Z < 0) or (targetAddr_Z >= self.getParam_NoCSizeZ()):
            assert False

        if portName == "IP":
            self._mainTopo[targetAddr_X][targetAddr_Y][targetAddr_Z].FIFOIPIn_deleteOneFlit()

        else:
            self._mainTopo[targetAddr_X][targetAddr_Y][targetAddr_Z].FIFO_deleteOneFlit_byPortName(portName=targetPortName)



    def Update_oneCycle_Step1(self):
        '''
        Run 1-cycle (1-step flits forwarding & FIFOs update)
        :return:
        '''
        for idx_zi in range(0, self.getParam_NoCSizeZ()):
            for idx_yi in range(0, self.getParam_NoCSizeY()):
                for idx_xi in range(0, self.getParam_NoCSizeX()):
                    # The current router
                    routerAddr = (copy.deepcopy(idx_xi), copy.deepcopy(idx_yi), copy.deepcopy(idx_zi))
                    # The input reqs to this router
                    inputReqs_list = [None]*7
                    inputReqs_list[0], inputFlit_IP = self.getRouterInput_byPortName(routerAddr=routerAddr, portName="IP")
                    inputReqs_list[1], inputFlit_W = self.getRouterInput_byPortName(routerAddr=routerAddr, portName="W")
                    inputReqs_list[2], inputFlit_E = self.getRouterInput_byPortName(routerAddr=routerAddr, portName="E")
                    inputReqs_list[3], inputFlit_S = self.getRouterInput_byPortName(routerAddr=routerAddr, portName="S")
                    inputReqs_list[4], inputFlit_N = self.getRouterInput_byPortName(routerAddr=routerAddr, portName="N")
                    inputReqs_list[5], inputFlit_D = self.getRouterInput_byPortName(routerAddr=routerAddr, portName="D")
                    inputReqs_list[6], inputFlit_U = self.getRouterInput_byPortName(routerAddr=routerAddr, portName="U")

                    inputReqs_tuple = tuple(inputReqs_list)

                    # Update Router
                    grantedInputReqs = self._mainTopo[idx_xi][idx_yi][idx_zi].router_updateNextCycle_Step1(inputReqs_tuple=inputReqs_tuple,
                                                                                  inputIP_tuple=inputFlit_IP,
                                                                                  inputW_tuple=inputFlit_W,
                                                                                  inputE_tuple=inputFlit_E,
                                                                                  inputS_tuple=inputFlit_S,
                                                                                  inputN_tuple=inputFlit_N,
                                                                                  inputD_tuple=inputFlit_D,
                                                                                  inputU_tuple=inputFlit_U)

                    # Update the output FIFO of neighboring routers
                    #IP
                    if grantedInputReqs[0] is True:
                        self.update_inputFlitReceived(routerAddr=routerAddr, portName="IP")
                    else:
                        assert grantedInputReqs[0] is False
                    # W
                    if grantedInputReqs[1] is True:
                        self.update_inputFlitReceived(routerAddr=routerAddr, portName="W")
                    else:
                        assert grantedInputReqs[1] is False
                    # E
                    if grantedInputReqs[2] is True:
                        self.update_inputFlitReceived(routerAddr=routerAddr, portName="E")
                    else:
                        assert grantedInputReqs[2] is False
                    # S
                    if grantedInputReqs[3] is True:
                        self.update_inputFlitReceived(routerAddr=routerAddr, portName="S")
                    else:
                        assert grantedInputReqs[3] is False
                    # N
                    if grantedInputReqs[4] is True:
                        self.update_inputFlitReceived(routerAddr=routerAddr, portName="N")
                    else:
                        assert grantedInputReqs[4] is False
                    # D
                    if grantedInputReqs[5] is True:
                        self.update_inputFlitReceived(routerAddr=routerAddr, portName="D")
                    else:
                        assert grantedInputReqs[5] is False
                    # U
                    if grantedInputReqs[6] is True:
                        self.update_inputFlitReceived(routerAddr=routerAddr, portName="U")
                    else:
                        assert grantedInputReqs[6] is False




    def Update_oneCycle_Step2(self):
        for idx_zi in range(0, self.getParam_NoCSizeZ()):
            for idx_yi in range(0, self.getParam_NoCSizeY()):
                for idx_xi in range(0, self.getParam_NoCSizeX()):
                    # # The current router
                    # routerAddr = (copy.deepcopy(idx_xi), copy.deepcopy(idx_yi), copy.deepcopy(idx_zi))
                    # # The input reqs to this router
                    # inputReqs_list = [None]*7
                    # inputReqs_list[0], inputFlit_IP = self.getRouterInput_byPortName(routerAddr=routerAddr, portName="IP")
                    # inputReqs_list[1], inputFlit_W = self.getRouterInput_byPortName(routerAddr=routerAddr, portName="W")
                    # inputReqs_list[2], inputFlit_E = self.getRouterInput_byPortName(routerAddr=routerAddr, portName="E")
                    # inputReqs_list[3], inputFlit_S = self.getRouterInput_byPortName(routerAddr=routerAddr, portName="S")
                    # inputReqs_list[4], inputFlit_N = self.getRouterInput_byPortName(routerAddr=routerAddr, portName="N")
                    # inputReqs_list[5], inputFlit_D = self.getRouterInput_byPortName(routerAddr=routerAddr, portName="D")
                    # inputReqs_list[6], inputFlit_U = self.getRouterInput_byPortName(routerAddr=routerAddr, portName="U")
                    #
                    # inputReqs_tuple = tuple(inputReqs_list)

                    # Update Router
                    self._mainTopo[idx_xi][idx_yi][idx_zi].router_updateNextCycle_Step2()

                    # # Update the output FIFO of neighboring routers
                    # #IP
                    # if grantedInputReqs[0] is True:
                    #     self.update_inputFlitReceived(routerAddr=routerAddr, portName="IP")
                    # else:
                    #     assert grantedInputReqs[0] is False
                    # # W
                    # if grantedInputReqs[1] is True:
                    #     self.update_inputFlitReceived(routerAddr=routerAddr, portName="W")
                    # else:
                    #     assert grantedInputReqs[1] is False
                    # # E
                    # if grantedInputReqs[2] is True:
                    #     self.update_inputFlitReceived(routerAddr=routerAddr, portName="E")
                    # else:
                    #     assert grantedInputReqs[2] is False
                    # # S
                    # if grantedInputReqs[3] is True:
                    #     self.update_inputFlitReceived(routerAddr=routerAddr, portName="S")
                    # else:
                    #     assert grantedInputReqs[3] is False
                    # # N
                    # if grantedInputReqs[4] is True:
                    #     self.update_inputFlitReceived(routerAddr=routerAddr, portName="N")
                    # else:
                    #     assert grantedInputReqs[4] is False
                    # # D
                    # if grantedInputReqs[5] is True:
                    #     self.update_inputFlitReceived(routerAddr=routerAddr, portName="D")
                    # else:
                    #     assert grantedInputReqs[5] is False
                    # # U
                    # if grantedInputReqs[6] is True:
                    #     self.update_inputFlitReceived(routerAddr=routerAddr, portName="U")
                    # else:
                    #     assert grantedInputReqs[6] is False

    def Update_oneCycle(self):
        self.Update_oneCycle_Step1()
        self.Update_oneCycle_Step2()


    def UpdateOneRouter_oneCycle(self, idx_xi, idx_yi, idx_zi):
        '''
        Run 1-cycle (1-step flits forwarding & FIFOs update)
        :return:
        '''

        # The current router
        routerAddr = (copy.deepcopy(idx_xi), copy.deepcopy(idx_yi), copy.deepcopy(idx_zi))
        # The input reqs to this router
        inputReqs_list = [None]*7
        inputReqs_list[0], inputFlit_IP = self.getRouterInput_byPortName(routerAddr=routerAddr, portName="IP")
        inputReqs_list[1], inputFlit_W = self.getRouterInput_byPortName(routerAddr=routerAddr, portName="W")
        inputReqs_list[2], inputFlit_E = self.getRouterInput_byPortName(routerAddr=routerAddr, portName="E")
        inputReqs_list[3], inputFlit_S = self.getRouterInput_byPortName(routerAddr=routerAddr, portName="S")
        inputReqs_list[4], inputFlit_N = self.getRouterInput_byPortName(routerAddr=routerAddr, portName="N")
        inputReqs_list[5], inputFlit_D = self.getRouterInput_byPortName(routerAddr=routerAddr, portName="D")
        inputReqs_list[6], inputFlit_U = self.getRouterInput_byPortName(routerAddr=routerAddr, portName="U")

        inputReqs_tuple = tuple(inputReqs_list)

        # Update Router
        grantedInputReqs = self._mainTopo[idx_xi][idx_yi][idx_zi].router_updateNextCycle_Step1(inputReqs_tuple=inputReqs_tuple,
                                                                      inputIP_tuple=inputFlit_IP,
                                                                      inputW_tuple=inputFlit_W,
                                                                      inputE_tuple=inputFlit_E,
                                                                      inputS_tuple=inputFlit_S,
                                                                      inputN_tuple=inputFlit_N,
                                                                      inputD_tuple=inputFlit_D,
                                                                      inputU_tuple=inputFlit_U)

        # Update the output FIFO of neighboring routers
        #IP
        if grantedInputReqs[0] is True:
            self.update_inputFlitReceived(routerAddr=routerAddr, portName="IP")
        else:
            assert grantedInputReqs[0] is False
        # W
        if grantedInputReqs[1] is True:
            self.update_inputFlitReceived(routerAddr=routerAddr, portName="W")
        else:
            assert grantedInputReqs[1] is False
        # E
        if grantedInputReqs[2] is True:
            self.update_inputFlitReceived(routerAddr=routerAddr, portName="E")
        else:
            assert grantedInputReqs[2] is False
        # S
        if grantedInputReqs[3] is True:
            self.update_inputFlitReceived(routerAddr=routerAddr, portName="S")
        else:
            assert grantedInputReqs[3] is False
        # N
        if grantedInputReqs[4] is True:
            self.update_inputFlitReceived(routerAddr=routerAddr, portName="N")
        else:
            assert grantedInputReqs[4] is False
        # D
        if grantedInputReqs[5] is True:
            self.update_inputFlitReceived(routerAddr=routerAddr, portName="D")
        else:
            assert grantedInputReqs[5] is False
        # U
        if grantedInputReqs[6] is True:
            self.update_inputFlitReceived(routerAddr=routerAddr, portName="U")
        else:
            assert grantedInputReqs[6] is False

        self._mainTopo[idx_xi][idx_yi][idx_zi].router_updateNextCycle_Step2()


    def Update_injectFlit(self, routerAddr, injectedFlit_tuple):
        '''
        Inject a flit into the IP-to-router FIFO connecting with the router with address routerAddr.
        :param routerAddr:
        :param injectedFlit_tuple:
        :return:
        '''
        assert isinstance(routerAddr, tuple) and (len(routerAddr) == 3)
        assert isinstance(injectedFlit_tuple, tuple)
        target_AddrX = copy.deepcopy(routerAddr[0])
        target_AddrY = copy.deepcopy(routerAddr[1])
        target_AddrZ = copy.deepcopy(routerAddr[2])
        self._mainTopo[target_AddrX][target_AddrY][target_AddrZ].FIFOIPIn_injectFlit(flitInjected=copy.deepcopy(injectedFlit_tuple))

    def export_IPReceivedFlits(self, routerAddr, filePathAndName_str, comment_str):
        '''
        Export the flits in the router-to-IP FIFOs. Note that the flit exported to file will also be deleted from the FIFO.
        :param filename_str:
        :param comment_str:
        :return:
        '''
        assert isinstance(routerAddr, tuple) and (len(routerAddr) == 3)
        target_AddrX = copy.deepcopy(routerAddr[0])
        target_AddrY = copy.deepcopy(routerAddr[1])
        target_AddrZ = copy.deepcopy(routerAddr[2])
        with open(filePathAndName_str, 'a') as f:
            while self._mainTopo[target_AddrX][target_AddrY][target_AddrZ].FIFO_checkIfEmpty_byPortName(portName="IP") is False:
                current_flit = self._mainTopo[target_AddrX][target_AddrY][target_AddrZ].FIFO_getFirstFlit_byPortName(portName="IP")
                current_flit_str = ' '.join(current_flit)
                f.write("[" + comment_str + "] - " + current_flit_str)
                self._mainTopo[target_AddrX][target_AddrY][target_AddrZ].FIFO_deleteOneFlit_byPortName(portName="IP")

    def readOut_IPReceivedFlits(self, routerAddr):
        '''
        Get the flits in the router-to-IP FIFOs. Note that the flit exported to file will also be deleted from the FIFO.
        :param routerAddr:
        :return:
        '''
        assert isinstance(routerAddr, tuple) and (len(routerAddr) == 3)
        target_AddrX = copy.deepcopy(routerAddr[0])
        target_AddrY = copy.deepcopy(routerAddr[1])
        target_AddrZ = copy.deepcopy(routerAddr[2])
        current_flit = self._mainTopo[target_AddrX][target_AddrY][target_AddrZ].FIFO_getFirstFlit_byPortName(portName="IP")
        if current_flit is not None:
            self._mainTopo[target_AddrX][target_AddrY][target_AddrZ].FIFO_deleteOneFlit_byPortName(portName="IP")
        return copy.deepcopy(current_flit)

    def readOnly_currentFlitIPSend(self, routerAddr):
        '''
        Get the flits in the IP-to-router FIFOs. Note that the flit exported to file will NOT be deleted from the FIFO.
        :param routerAddr:
        :return:
        '''
        assert isinstance(routerAddr, tuple) and (len(routerAddr) == 3)
        target_AddrX = copy.deepcopy(routerAddr[0])
        target_AddrY = copy.deepcopy(routerAddr[1])
        target_AddrZ = copy.deepcopy(routerAddr[2])
        current_flit = self._mainTopo[target_AddrX][target_AddrY][target_AddrZ].FIFOIPIn_getFirstFlit()
        return copy.deepcopy(current_flit)

    def readOnly_firstFlitInRouterOutFIFO(self, routerAddr, portName):
        '''
        Get the flits in the router FIFOs. Note that the flit exported to file will NOT be deleted from the FIFO.
        :param routerAddr:
        :param portName:
        :return:
        '''
        assert isinstance(routerAddr, tuple) and (len(routerAddr) == 3)
        target_AddrX = copy.deepcopy(routerAddr[0])
        target_AddrY = copy.deepcopy(routerAddr[1])
        target_AddrZ = copy.deepcopy(routerAddr[2])
        current_flit = self._mainTopo[target_AddrX][target_AddrY][target_AddrZ].FIFO_getFirstFlit_byPortName(portName=portName)
        return copy.deepcopy(current_flit)

    def readOnly_currentRouterStates(self, routerAddr):
        '''

        :param routerAddr:
        :return:bool(If locked), str(FW mode), tuple(If input ports enabled), tuple(If output ports enabled)
        '''
        assert isinstance(routerAddr, tuple) and (len(routerAddr) == 3)
        target_AddrX = copy.deepcopy(routerAddr[0])
        target_AddrY = copy.deepcopy(routerAddr[1])
        target_AddrZ = copy.deepcopy(routerAddr[2])
        rState_ifLocked, rState_FwMode, rState_inPortState, rState_outPortState = self._mainTopo[target_AddrX][target_AddrY][target_AddrZ].getRouterStates()
        return copy.deepcopy(rState_ifLocked), copy.deepcopy(rState_FwMode), copy.deepcopy(rState_inPortState), copy.deepcopy(rState_outPortState)

    def getFIFOState_ifEmpty_byLocalRouter_byPortName(self, localRouterAddr, portName):
        '''
        Return if the selected FIFO is empty.
        The localRouterAddr is the Local Router of FIFO.
        Assert portName in ("W", "E", "S", "N", "D", "U", "IPIn", "IPOut")
        :param localRouterAddr:
        :param portName:
        :return:
        '''
        assert portName in ("W_Out", "E_Out", "S_Out", "N_Out", "D_Out", "U_Out", "IP_In", "IP_Out")
        assert isinstance(localRouterAddr, tuple) and (len(localRouterAddr) == 3)
        target_AddrX = copy.deepcopy(localRouterAddr[0])
        target_AddrY = copy.deepcopy(localRouterAddr[1])
        target_AddrZ = copy.deepcopy(localRouterAddr[2])

        if portName == "W_Out":
            ifEmpty = self._mainTopo[target_AddrX][target_AddrY][target_AddrZ].FIFO_checkIfEmpty_byPortName(portName="W")

        elif portName == "E_Out":
            ifEmpty = self._mainTopo[target_AddrX][target_AddrY][target_AddrZ].FIFO_checkIfEmpty_byPortName(portName="E")

        elif portName == "S_Out":
            ifEmpty = self._mainTopo[target_AddrX][target_AddrY][target_AddrZ].FIFO_checkIfEmpty_byPortName(portName="S")

        elif portName == "N_Out":
            ifEmpty = self._mainTopo[target_AddrX][target_AddrY][target_AddrZ].FIFO_checkIfEmpty_byPortName(portName="N")

        elif portName == "D_Out":
            ifEmpty = self._mainTopo[target_AddrX][target_AddrY][target_AddrZ].FIFO_checkIfEmpty_byPortName(portName="D")

        elif portName == "U_Out":
            ifEmpty = self._mainTopo[target_AddrX][target_AddrY][target_AddrZ].FIFO_checkIfEmpty_byPortName(portName="U")

        elif portName == "IP_Out":
            ifEmpty = self._mainTopo[target_AddrX][target_AddrY][target_AddrZ].FIFO_checkIfEmpty_byPortName(portName="IP")

        else:
            ifEmpty = self._mainTopo[target_AddrX][target_AddrY][target_AddrZ].FIFOIPIn_checkIfEmpty()

        assert ifEmpty in (True, False)

        return ifEmpty

    def getNoCState_ifAllTaskCompleted(self):
        '''
        If all the forwarding tasks have been completed.
        :return: Bool, Tuple - If completed & The location of the flits being forwarded.
        '''
        if_noActiveTask = True
        activeTask_list = []
        for idx_xi in range(0, self.getParam_NoCSizeX()):
            for idx_yi in range(0, self.getParam_NoCSizeY()):
                for idx_zi in range(0, self.getParam_NoCSizeZ()):
                    for portName_i in ("W_Out", "E_Out", "S_Out", "N_Out", "D_Out", "U_Out", "IP_In"):
                        if self.getFIFOState_ifEmpty_byLocalRouter_byPortName(localRouterAddr=(copy.deepcopy(idx_xi), copy.deepcopy(idx_yi), copy.deepcopy(idx_zi)),
                                                                              portName=copy.deepcopy(portName_i)) is False:
                            if_noActiveTask = False
                            activeTask_list.append( ( copy.deepcopy(idx_xi), copy.deepcopy(idx_yi), copy.deepcopy(idx_zi),
                                                   copy.deepcopy(portName_i) ) )
        activeTask_tuple = tuple(copy.deepcopy(activeTask_list))
        return copy.deepcopy(if_noActiveTask), activeTask_tuple





########################################################################################################################
########################################################################################################################
class NoCTop_FP(NoCsTop_BASE):
    '''
    3D NoC (FP, no NC)

    '''
    def __init__(self, nX, nY, nZ, SimuConfig_instance):
        assert isinstance(nX, int) and (nX > 1)
        assert isinstance(nY, int) and (nY > 1)
        assert isinstance(nZ, int) and (nZ > 1)
        self._param_NoCSizeX = copy.deepcopy(nX)
        self._param_NoCSizeY = copy.deepcopy(nY)
        self._param_NoCSizeZ = copy.deepcopy(nZ)

        # assert isinstance(SimuConfig_instance, imported_ActiveConfiguration.SimuConfigs)
        self._param_SimuConfigInstance = copy.deepcopy(SimuConfig_instance)

        self._NoCTopologyInit()

    def _NoCTopologyInit(self):
        # self._mainTopo = [ [ [0]*(self.getParam_NoCSizeZ()) ]*(self.getParam_NoCSizeY()) ]*(self.getParam_NoCSizeX())
        self._mainTopo = []
        temp_list_y = []
        temp_list_z = []
        for idx_zi in range(0, self.getParam_NoCSizeZ()):
            temp_list_z.append(None)
        for idx_yi in range(0, self.getParam_NoCSizeY()):
            temp_list_y.append(copy.deepcopy(temp_list_z))
        for idx_xi in range(0, self.getParam_NoCSizeX()):
            self._mainTopo.append(copy.deepcopy(temp_list_y))

        router_id = 0
        for idx_xi in range(0, self.getParam_NoCSizeX()):
            for idx_yi in range(0, self.getParam_NoCSizeY()):
                for idx_zi in range(0, self.getParam_NoCSizeZ()):
                    # print(list(self._mainTopo))
                    # print(idx_xi, idx_yi, idx_zi)
                    # print(self._mainTopo[idx_xi][idx_yi][idx_zi])
                    assert self._mainTopo[idx_xi][idx_yi][idx_zi] == None
                    self._mainTopo[idx_xi][idx_yi][idx_zi] = Router_FIFO_FP_top(router_id=router_id,
                                                                                routerAddr_tuple=(copy.deepcopy(idx_xi), copy.deepcopy(idx_yi), copy.deepcopy(idx_zi)),
                                                                                SimuConfig_instance=self._param_SimuConfigInstance)
                    router_id = router_id + 1
        print("[NoCs_top/NoCTop_FP] NoC (FP) Topology Initialization - Size={}x{}x{}".format(self.getParam_NoCSizeX(),
                                                                                self.getParam_NoCSizeY(),
                                                                                self.getParam_NoCSizeZ()) )



class NoCTop_NCFP(NoCsTop_BASE):
    '''
    3D NoC (FP, with NC)

    '''
    def __init__(self, nX, nY, nZ, SimuConfig_instance):
        assert isinstance(nX, int) and (nX > 1)
        assert isinstance(nY, int) and (nY > 1)
        assert isinstance(nZ, int) and (nZ > 1)
        self._param_NoCSizeX = copy.deepcopy(nX)
        self._param_NoCSizeY = copy.deepcopy(nY)
        self._param_NoCSizeZ = copy.deepcopy(nZ)

        # assert isinstance(SimuConfig_instance, imported_ActiveConfiguration.SimuConfigs)
        self._param_SimuConfigInstance = copy.deepcopy(SimuConfig_instance)

        self._NoCTopologyInit()

    def _NoCTopologyInit(self):
        # self._mainTopo = [ [ [0]*(self.getParam_NoCSizeZ()) ]*(self.getParam_NoCSizeY()) ]*(self.getParam_NoCSizeX())
        self._mainTopo = []
        temp_list_y = []
        temp_list_z = []
        for idx_zi in range(0, self.getParam_NoCSizeZ()):
            temp_list_z.append(None)
        for idx_yi in range(0, self.getParam_NoCSizeY()):
            temp_list_y.append(copy.deepcopy(temp_list_z))
        for idx_xi in range(0, self.getParam_NoCSizeX()):
            self._mainTopo.append(copy.deepcopy(temp_list_y))

        router_id = 0
        for idx_xi in range(0, self.getParam_NoCSizeX()):
            for idx_yi in range(0, self.getParam_NoCSizeY()):
                for idx_zi in range(0, self.getParam_NoCSizeZ()):
                    # print(list(self._mainTopo))
                    # print(idx_xi, idx_yi, idx_zi)
                    # print(self._mainTopo[idx_xi][idx_yi][idx_zi])
                    assert self._mainTopo[idx_xi][idx_yi][idx_zi] == None
                    self._mainTopo[idx_xi][idx_yi][idx_zi] = Router_FIFO_NCFP_top(router_id=router_id,
                                                                                routerAddr_tuple=(copy.deepcopy(idx_xi), copy.deepcopy(idx_yi), copy.deepcopy(idx_zi)),
                                                                                SimuConfig_instance=self._param_SimuConfigInstance)
                    router_id = router_id + 1
        print("[NoCs_top/NoCTop_NCFP] NoC (NCFP) Topology Initialization - Size={}x{}x{}".format(self.getParam_NoCSizeX(),
                                                                                self.getParam_NoCSizeY(),
                                                                                self.getParam_NoCSizeZ()) )











########################################################################################################################
########################################################################################################################
# class _NoCTopoElement_routersFP_1D:
#     def __init__(self, nX, addr_YAxis, addr_ZAxis, SimuConfig_instance):
#         assert (isinstance(nX, int) and (nX > 2))
#         self._topoParam_nx = copy.deepcopy(nX)
#
#         assert isinstance(addr_YAxis, int)
#         assert isinstance(addr_ZAxis, int)
#         self._topoParam_addrYAxis = copy.deepcopy(addr_YAxis)
#         self._topoParam_addrZAxis = copy.deepcopy(addr_ZAxis)
#
#         assert isinstance(SimuConfig_instance, imported_ActiveConfiguration.SimuConfigs)
#         self._topo_reset(SimuConfig_instance=SimuConfig_instance)
#
#     def getParam_addrY(self):
#         return copy.deepcopy(self._topoParam_addrYAxis)
#
#     def getParam_addrZ(self):
#         return copy.deepcopy(self._topoParam_addrZAxis)
#
#     def getParam_nx(self):
#         return copy.deepcopy(self._topoParam_nx)
#
#     def _topo_reset(self, SimuConfig_instance):
#         self._mainTopo_list = []
#         for idx_i in range(0, self.getParam_nx()):
#             current_router_addr = (copy.deepcopy(idx_i), self.getParam_addrY(), self.getParam_addrZ())
#             # self._mainTopo_list.append(imported_Routers_top.RoutersTop_FP(router_id=copy.deepcopy(idx_i), routerAddr_tuple=copy.deepcopy(current_router_addr), SimuConfig_instance=SimuConfig_instance))
#             self._mainTopo_list.append(Router_FIFO_FP_top(router_id=copy.deepcopy(idx_i), routerAddr_tuple=copy.deepcopy(current_router_addr), SimuConfig_instance=SimuConfig_instance))
#
#     # def update_router(self, router_idx, fifoStates_tuple, inputReqs_tuple,
#     #                  inputIP_tuple, inputW_tuple, inputE_tuple, inputS_tuple, inputN_tuple, inputD_tuple, inputU_tuple):
#     #     assert isinstance(router_idx, int)
#     #     activeIn_tuple, activeOut_tuple, outIP_tuple, outW_tuple, outE_tuple, outS_tuple, outN_tuple, outD_tuple, outU_tuple = self._mainTopo_list[router_idx].run_nextCycle(fifoStates_tuple=fifoStates_tuple,
#     #                                                                                                                                                                          inputReqs_tuple=inputReqs_tuple,
#     #                                                                                                                                                                          inputIP_tuple=inputIP_tuple,
#     #                                                                                                                                                                          inputW_tuple=inputW_tuple,
#     #                                                                                                                                                                          inputE_tuple=inputE_tuple,
#     #                                                                                                                                                                          inputS_tuple=inputS_tuple,
#     #                                                                                                                                                                          inputN_tuple=inputN_tuple,
#     #                                                                                                                                                                          inputD_tuple=inputD_tuple,
#     #                                                                                                                                                                          inputU_tuple=inputU_tuple)
#     #     return activeIn_tuple, activeOut_tuple, outIP_tuple, outW_tuple, outE_tuple, outS_tuple, outN_tuple, outD_tuple, outU_tuple
#     def get_routerAddr(self, router_idx):
#         assert isinstance(router_idx, int)
#         return copy.deepcopy(self._mainTopo_list[router_idx].getParam_address())
#     def update_router(self, router_idx, inputReqs_tuple,
#                       inputIP_tuple, inputW_tuple, inputE_tuple, inputS_tuple, inputN_tuple, inputD_tuple, inputU_tuple,
#                       addr_assert_tuple=None):
#         '''
#         Update the state of a router. The optional 'addr_assert_tuple' is the address of the router, used to check if the selected router is the one you want to update.
#
#         :param router_idx:int
#         :param inputReqs_tuple: tuple(bool, bool, bool, bool, bool, bool, bool) - If the reqs from (IP, W, E, S, N, D, U) are available.
#         :param inputIP_tuple: None or tuple(bool, bool, ...) - A flit. Default value is None.
#         :param inputW_tuple: None or tuple(bool, bool, ...) - A flit. Default value is None.
#         :param inputE_tuple: None or tuple(bool, bool, ...) - A flit. Default value is None.
#         :param inputS_tuple: None or tuple(bool, bool, ...) - A flit. Default value is None.
#         :param inputN_tuple: None or tuple(bool, bool, ...) - A flit. Default value is None.
#         :param inputD_tuple: None or tuple(bool, bool, ...) - A flit. Default value is None.
#         :param inputU_tuple: None or tuple(bool, bool, ...) - A flit. Default value is None.
#         :param addr_assert_tuple: tuple(int, int, int) - (address_X, addressY, address_Z).
#         :return: activeIn_tuple
#         '''
#         if addr_assert_tuple is not None:
#             assert addr_assert_tuple == self.get_routerAddr(router_idx=router_idx)
#
#         activeIn_tuple = self._mainTopo_list[router_idx].update_nextCycle(inputReqs_tuple=inputReqs_tuple,
#                                                                           inputIP_tuple=inputIP_tuple,
#                                                                           inputW_tuple=inputW_tuple,
#                                                                           inputE_tuple=inputE_tuple,
#                                                                           inputS_tuple=inputS_tuple,
#                                                                           inputN_tuple=inputN_tuple,
#                                                                           inputD_tuple=inputD_tuple,
#                                                                           inputU_tuple=inputU_tuple)
#         return copy.deepcopy(activeIn_tuple)
#
#     def FIFO_getFirstFlit(self, router_idx, FIFO_name, addr_assert_tuple=None):
#         '''
#         Get the first flit of a FIFO. The optional 'addr_assert_tuple' is the address of the router, used to check if the selected router is the one you want to update.
#         Each router has 7 FIFOs, which are named as "IP", "W", "E", "S", "N", "D" and "U", respectively.
#
#         :param router_idx:
#         :param FIFO_name:
#         :param addr_assert_tuple:
#         :return: tuple(bool, bool, ...)
#         '''
#         assert FIFO_name in ("IP", "W", "E", "S", "N", "D", "U")
#         if addr_assert_tuple is not None:
#             assert addr_assert_tuple == self.get_routerAddr(router_idx=router_idx)
#         return copy.deepcopy(self._mainTopo_list[router_idx].getFIFOFirstFlit_byPortName(portName=copy.deepcopy(FIFO_name)))
#
#     def FIFO_deleteFirstFlit(self, router_idx, FIFO_name, addr_assert_tuple=None):
#         '''
#         Delete the first flit of a FIFO. The optional 'addr_assert_tuple' is the address of the router, used to check if the selected router is the one you want to update.
#         :param router_idx:
#         :param FIFO_name:
#         :param addr_assert_tuple:
#         :return:
#         '''
#         assert FIFO_name in ("IP", "W", "E", "S", "N", "D", "U")
#         if addr_assert_tuple is not None:
#             assert addr_assert_tuple == self.get_routerAddr(router_idx=router_idx)
#         self._mainTopo_list[router_idx].updateFIFO_deleteOneFlit(portName=copy.deepcopy(FIFO_name))
#
#
#
#
#
#
#

########################################################################################################################
########################################################################################################################
# class NoCsTop_FP(NoCsTop_BASE):
#     def __init__(self, n_X, n_Y, n_Z, SimuConfig_instance_userDefined):
#         assert (isinstance(n_X, int) and (n_X > 2))
#         assert (isinstance(n_Y, int) and (n_Y > 2))
#         assert (isinstance(n_Z, int) and (n_Z > 2))
#
#         self._param_nX = copy.deepcopy(n_X)
#         self._param_nY = copy.deepcopy(n_Y)
#         self._param_nZ = copy.deepcopy(n_Z)
#
#         assert isinstance(SimuConfig_instance_userDefined, imported_ActiveConfiguration.SimuConfigs)
#         self._param_SimuConfig = copy.deepcopy(SimuConfig_instance_userDefined)
#
#     def getParam_NoCSize(self):
#         return copy.deepcopy(self._param_nX), copy.deepcopy(self._param_nY), copy.deepcopy(self._param_nZ)
#
#     def _NoCTopology_build(self):
#         '''
#         + 1D Network (X-axis):
#         #\n
#         #   router tuple: routers_1D = (R0, R1, R2, ..., R{nX-1}), the number of elements equals to (self.getParam_NoCSize()[0])\n
#         #\n
#         #   fifo tuple (L->R): fifos_1D_LR = (F01, F12, F23, ...F{nX-2}{nX-1}), the number of elements equals to (self.getParam_NoCSize()[0] - 1)\n
#         #\n
#         #   fifo tuple (R->L): fifos_1D_RL = (F10, F21, F32, ...F{nX-1}{nX-2}), the number of elements equals to (self.getParam_NoCSize()[0] - 1)\n
#         #\n
#         #   A 1D Network: topo_1D = (routers_1D, fifos_1D_LR, fifos_1D_RL)
#
#         + 2D Network (XY-axis):
#         #   (topo_1D) - (fifos_2D) - (topo_1D) - (fifos_2D) - (topo_1D) - ...\n
#         #\n
#         #   Y-axis connections (S->N): fifos_2D_SN = (FX0_SN, FX1_SN, FX2_SN, ..., FX{nX-1}_SN), the number of elements equals to (self.getParam_NoCSize()[0])\n
#         #\n
#         #   Y-axis connections (N->S): fifos_2D_NS = (FX0_NS, FX1_NS, FX2_NS, ..., FX{nX-1}_NS), the number of elements equals to (self.getParam_NoCSize()[0])\n
#         #\n
#         #   A 2D Network: topo_2D = (topo_1D_0, fifos_2D_SN_01, fifos_2D_NS_10, topo_1D_1, fifos_2D_SN_12, fifos_2D_NS_21, topo_1D_2, ..., fifos_2D_SN_{nY-2}{nY-1}, fifos_2D_NS_{nY-1}{nY-2}, topo_1D_{nY-1}), the number of elements equals to (3*self.getParam_NoCSize()[1] - 2)\n
#
#         + 3D Network (XYZ-axis):
#         #   (topo_2D) - (fifos_3D) - (topo_2D) - (fifos_3D) - (topo_2D) - ... \n
#         #\n
#         #   Z-axis connections: fifos_3D = (FY0s, FY1s, FY2s, ...FY{nY-1}s), in which FY{i}s = (FX0, FX1, FX2, ..., FX{nX-1}).\n
#         #\n
#         #   A 3D Network: topo_3D = (topo_2D_0, fifos_3D_01, topo_2D_1, fifos_3D_12, topo_2D_2, ..., fifos_3D_{nZ-2}{nZ-1}, topo_2D_{nZ-1}), the number of elements equals to (2*self.getParam_NoCSize()[2] - 1)\n
#
#
#
#         :return:
#         '''
