import copy

import NoC_Designs.Routers_top as imported_Routers_top
import NoC_Designs.FIFOs_top as imported_FIFOs_top
import Simulation.SimuConfigurationClass as imported_ActiveConfiguration

########################################################################################################################
########################################################################################################################
class NoCsTop_BASE:
    def __init__(self):
        assert False

########################################################################################################################
########################################################################################################################
class Router_FIFO_FP_top:
    def __init__(self, router_id, routerAddr_tuple, SimuConfig_instance):
        assert isinstance(SimuConfig_instance, imported_ActiveConfiguration.SimuConfigs)
        self._param_router_id = copy.deepcopy(router_id)
        self._param_routerAddr_tuple = copy.deepcopy(routerAddr_tuple)
        self._param_SimuConfig = SimuConfig_instance

        self._mainRouterInstance = imported_Routers_top.RoutersTop_FP(router_id=copy.deepcopy(router_id), routerAddr_tuple=copy.deepcopy(routerAddr_tuple), SimuConfig_instance=SimuConfig_instance)

        self._mainFIFOInstance_outIP = imported_FIFOs_top.FIFOsTop(
            flit_depth=SimuConfig_instance.getParam_FIFOFlitDepth(),
            flit_bw=SimuConfig_instance.getParam_flitBitWidth(), fifo_id=0)

        self._mainFIFOInstance_outW = imported_FIFOs_top.FIFOsTop(
            flit_depth=SimuConfig_instance.getParam_FIFOFlitDepth(),
            flit_bw=SimuConfig_instance.getParam_flitBitWidth(), fifo_id=1)

        self._mainFIFOInstance_outE = imported_FIFOs_top.FIFOsTop(
            flit_depth=SimuConfig_instance.getParam_FIFOFlitDepth(),
            flit_bw=SimuConfig_instance.getParam_flitBitWidth(), fifo_id=2)

        self._mainFIFOInstance_outS = imported_FIFOs_top.FIFOsTop(
            flit_depth=SimuConfig_instance.getParam_FIFOFlitDepth(),
            flit_bw=SimuConfig_instance.getParam_flitBitWidth(), fifo_id=3)

        self._mainFIFOInstance_outN = imported_FIFOs_top.FIFOsTop(
            flit_depth=SimuConfig_instance.getParam_FIFOFlitDepth(),
            flit_bw=SimuConfig_instance.getParam_flitBitWidth(), fifo_id=4)

        self._mainFIFOInstance_outD = imported_FIFOs_top.FIFOsTop(
            flit_depth=SimuConfig_instance.getParam_FIFOFlitDepth(),
            flit_bw=SimuConfig_instance.getParam_flitBitWidth(), fifo_id=5)

        self._mainFIFOInstance_outU = imported_FIFOs_top.FIFOsTop(
            flit_depth=SimuConfig_instance.getParam_FIFOFlitDepth(),
            flit_bw=SimuConfig_instance.getParam_flitBitWidth(), fifo_id=6)
    ####################################################################################################################
    def reset_all(self):
        self._mainRouterInstance = imported_Routers_top.RoutersTop_FP(router_id=copy.deepcopy(self._param_router_id),
                                                                      routerAddr_tuple=copy.deepcopy(self._param_routerAddr_tuple),
                                                                      SimuConfig_instance=self._param_SimuConfig)

        self._mainFIFOInstance_outIP = imported_FIFOs_top.FIFOsTop(
            flit_depth=self._param_SimuConfig.getParam_FIFOFlitDepth(),
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
    ####################################################################################################################
    def getParam_address(self):
        return copy.deepcopy(self._param_routerAddr_tuple)
    ####################################################################################################################
    def update_nextCycle(self, inputReqs_tuple,
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

        if activeOut_tuple[0] is True:
            self._mainFIFOInstance_outIP.memOp_writeOneFlit(flitNew=copy.deepcopy(outIP_tuple))
        else:
            assert activeOut_tuple[0] is False

        if activeOut_tuple[1] is True:
            self._mainFIFOInstance_outW.memOp_writeOneFlit(flitNew=copy.deepcopy(outW_tuple))
        else:
            assert activeOut_tuple[1] is False

        if activeOut_tuple[2] is True:
            self._mainFIFOInstance_outE.memOp_writeOneFlit(flitNew=copy.deepcopy(outE_tuple))
        else:
            assert activeOut_tuple[2] is False

        if activeOut_tuple[3] is True:
            self._mainFIFOInstance_outS.memOp_writeOneFlit(flitNew=copy.deepcopy(outS_tuple))
        else:
            assert activeOut_tuple[3] is False

        if activeOut_tuple[4] is True:
            self._mainFIFOInstance_outN.memOp_writeOneFlit(flitNew=copy.deepcopy(outN_tuple))
        else:
            assert activeOut_tuple[4] is False

        if activeOut_tuple[5] is True:
            self._mainFIFOInstance_outD.memOp_writeOneFlit(flitNew=copy.deepcopy(outD_tuple))
        else:
            assert activeOut_tuple[5] is False

        if activeOut_tuple[6] is True:
            self._mainFIFOInstance_outU.memOp_writeOneFlit(flitNew=copy.deepcopy(outU_tuple))
        else:
            assert activeOut_tuple[6] is False

        return copy.deepcopy(activeIn_tuple)

    ####################################################################################################################
    def getFIFOFirstFlit_byPortName(self, portName):
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
    def updateFIFO_deleteOneFlit(self, portName):
        if portName == "IP":
            self._mainFIFOInstance_outIP.memOp_deleteFirstFlit()
        elif portName == "W":
            self._mainFIFOInstance_outW.memOp_deleteFirstFlit()
        elif portName == "E":
            self._mainFIFOInstance_outE.memOp_deleteFirstFlit()
        elif portName == "S":
            self._mainFIFOInstance_outS.memOp_deleteFirstFlit()
        elif portName == "N":
            self._mainFIFOInstance_outN.memOp_deleteFirstFlit()
        elif portName == "D":
            self._mainFIFOInstance_outD.memOp_deleteFirstFlit()
        elif portName == "U":
            self._mainFIFOInstance_outU.memOp_deleteFirstFlit()
        else:
            assert False







########################################################################################################################
########################################################################################################################
class _NoCTopoElement_routersFP_1D:
    def __init__(self, nX, addr_YAxis, addr_ZAxis, SimuConfig_instance):
        assert (isinstance(nX, int) and (nX > 2))
        self._topoParam_nx = copy.deepcopy(nX)

        assert isinstance(addr_YAxis, int)
        assert isinstance(addr_ZAxis, int)
        self._topoParam_addrYAxis = copy.deepcopy(addr_YAxis)
        self._topoParam_addrZAxis = copy.deepcopy(addr_ZAxis)

        assert isinstance(SimuConfig_instance, imported_ActiveConfiguration.SimuConfigs)
        self._topo_reset(SimuConfig_instance=SimuConfig_instance)

    def getParam_addrY(self):
        return copy.deepcopy(self._topoParam_addrYAxis)

    def getParam_addrZ(self):
        return copy.deepcopy(self._topoParam_addrZAxis)

    def getParam_nx(self):
        return copy.deepcopy(self._topoParam_nx)

    def _topo_reset(self, SimuConfig_instance):
        self._mainTopo_list = []
        for idx_i in range(0, self.getParam_nx()):
            current_router_addr = (copy.deepcopy(idx_i), self.getParam_addrY(), self.getParam_addrZ())
            # self._mainTopo_list.append(imported_Routers_top.RoutersTop_FP(router_id=copy.deepcopy(idx_i), routerAddr_tuple=copy.deepcopy(current_router_addr), SimuConfig_instance=SimuConfig_instance))
            self._mainTopo_list.append(Router_FIFO_FP_top(router_id=copy.deepcopy(idx_i), routerAddr_tuple=copy.deepcopy(current_router_addr), SimuConfig_instance=SimuConfig_instance))

    # def update_router(self, router_idx, fifoStates_tuple, inputReqs_tuple,
    #                  inputIP_tuple, inputW_tuple, inputE_tuple, inputS_tuple, inputN_tuple, inputD_tuple, inputU_tuple):
    #     assert isinstance(router_idx, int)
    #     activeIn_tuple, activeOut_tuple, outIP_tuple, outW_tuple, outE_tuple, outS_tuple, outN_tuple, outD_tuple, outU_tuple = self._mainTopo_list[router_idx].run_nextCycle(fifoStates_tuple=fifoStates_tuple,
    #                                                                                                                                                                          inputReqs_tuple=inputReqs_tuple,
    #                                                                                                                                                                          inputIP_tuple=inputIP_tuple,
    #                                                                                                                                                                          inputW_tuple=inputW_tuple,
    #                                                                                                                                                                          inputE_tuple=inputE_tuple,
    #                                                                                                                                                                          inputS_tuple=inputS_tuple,
    #                                                                                                                                                                          inputN_tuple=inputN_tuple,
    #                                                                                                                                                                          inputD_tuple=inputD_tuple,
    #                                                                                                                                                                          inputU_tuple=inputU_tuple)
    #     return activeIn_tuple, activeOut_tuple, outIP_tuple, outW_tuple, outE_tuple, outS_tuple, outN_tuple, outD_tuple, outU_tuple
    def get_routerAddr(self, router_idx):
        assert isinstance(router_idx, int)
        return copy.deepcopy(self._mainTopo_list[router_idx].getParam_address())
    def update_router(self, router_idx, inputReqs_tuple,
                      inputIP_tuple, inputW_tuple, inputE_tuple, inputS_tuple, inputN_tuple, inputD_tuple, inputU_tuple,
                      addr_assert_tuple=None):
        '''
        Update the state of a router. The optional 'addr_assert_tuple' is the address of the router, used to check if the selected router is the one you want to update.

        :param router_idx:int
        :param inputReqs_tuple: tuple(bool, bool, bool, bool, bool, bool, bool) - If the reqs from (IP, W, E, S, N, D, U) are available.
        :param inputIP_tuple: None or tuple(bool, bool, ...) - A flit. Default value is None.
        :param inputW_tuple: None or tuple(bool, bool, ...) - A flit. Default value is None.
        :param inputE_tuple: None or tuple(bool, bool, ...) - A flit. Default value is None.
        :param inputS_tuple: None or tuple(bool, bool, ...) - A flit. Default value is None.
        :param inputN_tuple: None or tuple(bool, bool, ...) - A flit. Default value is None.
        :param inputD_tuple: None or tuple(bool, bool, ...) - A flit. Default value is None.
        :param inputU_tuple: None or tuple(bool, bool, ...) - A flit. Default value is None.
        :param addr_assert_tuple: tuple(int, int, int) - (address_X, addressY, address_Z).
        :return: activeIn_tuple
        '''
        if addr_assert_tuple is not None:
            assert addr_assert_tuple == self.get_routerAddr(router_idx=router_idx)

        activeIn_tuple = self._mainTopo_list[router_idx].update_nextCycle(inputReqs_tuple=inputReqs_tuple,
                                                                          inputIP_tuple=inputIP_tuple,
                                                                          inputW_tuple=inputW_tuple,
                                                                          inputE_tuple=inputE_tuple,
                                                                          inputS_tuple=inputS_tuple,
                                                                          inputN_tuple=inputN_tuple,
                                                                          inputD_tuple=inputD_tuple,
                                                                          inputU_tuple=inputU_tuple)
        return copy.deepcopy(activeIn_tuple)

    def FIFO_getFirstFlit(self, router_idx, FIFO_name, addr_assert_tuple=None):
        '''
        Get the first flit of a FIFO. The optional 'addr_assert_tuple' is the address of the router, used to check if the selected router is the one you want to update.
        Each router has 7 FIFOs, which are named as "IP", "W", "E", "S", "N", "D" and "U", respectively.

        :param router_idx:
        :param FIFO_name:
        :param addr_assert_tuple:
        :return: tuple(bool, bool, ...)
        '''
        assert FIFO_name in ("IP", "W", "E", "S", "N", "D", "U")
        if addr_assert_tuple is not None:
            assert addr_assert_tuple == self.get_routerAddr(router_idx=router_idx)
        return copy.deepcopy(self._mainTopo_list[router_idx].getFIFOFirstFlit_byPortName(portName=copy.deepcopy(FIFO_name)))

    def FIFO_deleteFirstFlit(self, router_idx, FIFO_name, addr_assert_tuple=None):
        '''
        Delete the first flit of a FIFO. The optional 'addr_assert_tuple' is the address of the router, used to check if the selected router is the one you want to update.
        :param router_idx:
        :param FIFO_name:
        :param addr_assert_tuple:
        :return:
        '''
        assert FIFO_name in ("IP", "W", "E", "S", "N", "D", "U")
        if addr_assert_tuple is not None:
            assert addr_assert_tuple == self.get_routerAddr(router_idx=router_idx)
        self._mainTopo_list[router_idx].updateFIFO_deleteOneFlit(portName=copy.deepcopy(FIFO_name))








########################################################################################################################
########################################################################################################################
class NoCsTop_FP(NoCsTop_BASE):
    def __init__(self, n_X, n_Y, n_Z, SimuConfig_instance_userDefined):
        assert (isinstance(n_X, int) and (n_X > 2))
        assert (isinstance(n_Y, int) and (n_Y > 2))
        assert (isinstance(n_Z, int) and (n_Z > 2))

        self._param_nX = copy.deepcopy(n_X)
        self._param_nY = copy.deepcopy(n_Y)
        self._param_nZ = copy.deepcopy(n_Z)

        assert isinstance(SimuConfig_instance_userDefined, imported_ActiveConfiguration.SimuConfigs)
        self._param_SimuConfig = copy.deepcopy(SimuConfig_instance_userDefined)

    def getParam_NoCSize(self):
        return copy.deepcopy(self._param_nX), copy.deepcopy(self._param_nY), copy.deepcopy(self._param_nZ)

    def _NoCTopology_build(self):
        '''
        + 1D Network (X-axis):
        #\n
        #   router tuple: routers_1D = (R0, R1, R2, ..., R{nX-1}), the number of elements equals to (self.getParam_NoCSize()[0])\n
        #\n
        #   fifo tuple (L->R): fifos_1D_LR = (F01, F12, F23, ...F{nX-2}{nX-1}), the number of elements equals to (self.getParam_NoCSize()[0] - 1)\n
        #\n
        #   fifo tuple (R->L): fifos_1D_RL = (F10, F21, F32, ...F{nX-1}{nX-2}), the number of elements equals to (self.getParam_NoCSize()[0] - 1)\n
        #\n
        #   A 1D Network: topo_1D = (routers_1D, fifos_1D_LR, fifos_1D_RL)

        + 2D Network (XY-axis):
        #   (topo_1D) - (fifos_2D) - (topo_1D) - (fifos_2D) - (topo_1D) - ...\n
        #\n
        #   Y-axis connections (S->N): fifos_2D_SN = (FX0_SN, FX1_SN, FX2_SN, ..., FX{nX-1}_SN), the number of elements equals to (self.getParam_NoCSize()[0])\n
        #\n
        #   Y-axis connections (N->S): fifos_2D_NS = (FX0_NS, FX1_NS, FX2_NS, ..., FX{nX-1}_NS), the number of elements equals to (self.getParam_NoCSize()[0])\n
        #\n
        #   A 2D Network: topo_2D = (topo_1D_0, fifos_2D_SN_01, fifos_2D_NS_10, topo_1D_1, fifos_2D_SN_12, fifos_2D_NS_21, topo_1D_2, ..., fifos_2D_SN_{nY-2}{nY-1}, fifos_2D_NS_{nY-1}{nY-2}, topo_1D_{nY-1}), the number of elements equals to (3*self.getParam_NoCSize()[1] - 2)\n

        + 3D Network (XYZ-axis):
        #   (topo_2D) - (fifos_3D) - (topo_2D) - (fifos_3D) - (topo_2D) - ... \n
        #\n
        #   Z-axis connections: fifos_3D = (FY0s, FY1s, FY2s, ...FY{nY-1}s), in which FY{i}s = (FX0, FX1, FX2, ..., FX{nX-1}).\n
        #\n
        #   A 3D Network: topo_3D = (topo_2D_0, fifos_3D_01, topo_2D_1, fifos_3D_12, topo_2D_2, ..., fifos_3D_{nZ-2}{nZ-1}, topo_2D_{nZ-1}), the number of elements equals to (2*self.getParam_NoCSize()[2] - 1)\n



        :return:
        '''
