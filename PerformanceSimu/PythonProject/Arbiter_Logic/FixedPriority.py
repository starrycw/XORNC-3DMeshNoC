# The core logic of the Fixed Priority Arbiter
import copy

import Arbiter_Logic.arbiterModules as arbiterModules

def arbiterLogic_fixedPriority(addrLocal_tuple, fifoStates_tuple, reqIP_tuple, reqW_tuple, reqE_tuple, reqS_tuple, reqN_tuple, reqD_tuple, reqU_tuple):
    '''
    The core logic of the Fixed Priority Arbiter - Main \n
    grants_tuple: tuple(bool, bool, bool, bool, bool, bool, bool) - The reqs from (IP, W, E, S, N, D, U) will be processed. \n
    forwards_tuple: tuple(bool, bool, bool, bool, bool, bool, bool) - The forward directions are (IP, W, E, S, N, D, U).

    :param addrLocal_tuple: tuple(int, int, int) - (addressX, addressY, addressZ)
    :param fifoStates_tuple: tuple(bool, bool, bool, bool, bool, bool, bool) - If the output fifos of (IP, W, E, S, N, D, U) has free space.
    :param reqIP_tuple: tuple(bool, int, int, int) - (if_req_available, addressX, addressY, addressZ)
    :param reqW_tuple: tuple(bool, int, int, int) - (if_req_available, addressX, addressY, addressZ)
    :param reqE_tuple: tuple(bool, int, int, int) - (if_req_available, addressX, addressY, addressZ)
    :param reqS_tuple: tuple(bool, int, int, int) - (if_req_available, addressX, addressY, addressZ)
    :param reqN_tuple: tuple(bool, int, int, int) - (if_req_available, addressX, addressY, addressZ)
    :param reqD_tuple: tuple(bool, int, int, int) - (if_req_available, addressX, addressY, addressZ)
    :param reqU_tuple: tuple(bool, int, int, int) - (if_req_available, addressX, addressY, addressZ)
    :return: grants_tuple, forwards_tuple
    '''

    assert isinstance(addrLocal_tuple, tuple) and len(addrLocal_tuple) == 3
    assert isinstance(fifoStates_tuple, tuple) and len(fifoStates_tuple) == 7
    assert isinstance(reqIP_tuple, tuple) and len(reqIP_tuple) == 4
    assert isinstance(reqW_tuple, tuple) and len(reqW_tuple) == 4
    assert isinstance(reqE_tuple, tuple) and len(reqE_tuple) == 4
    assert isinstance(reqS_tuple, tuple) and len(reqS_tuple) == 4
    assert isinstance(reqN_tuple, tuple) and len(reqN_tuple) == 4
    assert isinstance(reqD_tuple, tuple) and len(reqD_tuple) == 4
    assert isinstance(reqU_tuple, tuple) and len(reqU_tuple) == 4

    # Compare addresses
    addrCompare_IP = arbiterModules.arbiterModule_addrCompare(addrLocal_tuple=addrLocal_tuple,
                                                              addrDes_tuple=reqIP_tuple[1:4])
    addrCompare_W = arbiterModules.arbiterModule_addrCompare(addrLocal_tuple=addrLocal_tuple,
                                                              addrDes_tuple=reqW_tuple[1:4])
    addrCompare_E = arbiterModules.arbiterModule_addrCompare(addrLocal_tuple=addrLocal_tuple,
                                                             addrDes_tuple=reqE_tuple[1:4])
    addrCompare_S = arbiterModules.arbiterModule_addrCompare(addrLocal_tuple=addrLocal_tuple,
                                                             addrDes_tuple=reqS_tuple[1:4])
    addrCompare_N = arbiterModules.arbiterModule_addrCompare(addrLocal_tuple=addrLocal_tuple,
                                                             addrDes_tuple=reqN_tuple[1:4])
    addrCompare_D = arbiterModules.arbiterModule_addrCompare(addrLocal_tuple=addrLocal_tuple,
                                                             addrDes_tuple=reqD_tuple[1:4])
    addrCompare_U = arbiterModules.arbiterModule_addrCompare(addrLocal_tuple=addrLocal_tuple,
                                                             addrDes_tuple=reqU_tuple[1:4])

    # XYZ Routing
    IP_forwardXYZ_target = arbiterModules.arbiterModule_routingAlg_XYZ(addrCompare_tuple=addrCompare_IP)
    W_forwardXYZ_target = arbiterModules.arbiterModule_routingAlg_XYZ(addrCompare_tuple=addrCompare_W)
    E_forwardXYZ_target = arbiterModules.arbiterModule_routingAlg_XYZ(addrCompare_tuple=addrCompare_E)
    S_forwardXYZ_target = arbiterModules.arbiterModule_routingAlg_XYZ(addrCompare_tuple=addrCompare_S)
    N_forwardXYZ_target = arbiterModules.arbiterModule_routingAlg_XYZ(addrCompare_tuple=addrCompare_N)
    D_forwardXYZ_target = arbiterModules.arbiterModule_routingAlg_XYZ(addrCompare_tuple=addrCompare_D)
    U_forwardXYZ_target = arbiterModules.arbiterModule_routingAlg_XYZ(addrCompare_tuple=addrCompare_U)

    # Forwarding directions check
    IP_forwarding_ifallsat, IP_forwarding_sat, IP_forwarding_unsat = arbiterModules.arbiterModule_reqsCheck(
        forwardDirections_tuple=IP_forwardXYZ_target, directionStates_tuple=fifoStates_tuple)
    W_forwarding_ifallsat, W_forwarding_sat, W_forwarding_unsat = arbiterModules.arbiterModule_reqsCheck(
        forwardDirections_tuple=W_forwardXYZ_target, directionStates_tuple=fifoStates_tuple)
    E_forwarding_ifallsat, E_forwarding_sat, E_forwarding_unsat = arbiterModules.arbiterModule_reqsCheck(
        forwardDirections_tuple=E_forwardXYZ_target, directionStates_tuple=fifoStates_tuple)
    S_forwarding_ifallsat, S_forwarding_sat, S_forwarding_unsat = arbiterModules.arbiterModule_reqsCheck(
        forwardDirections_tuple=S_forwardXYZ_target, directionStates_tuple=fifoStates_tuple)
    N_forwarding_ifallsat, N_forwarding_sat, N_forwarding_unsat = arbiterModules.arbiterModule_reqsCheck(
        forwardDirections_tuple=N_forwardXYZ_target, directionStates_tuple=fifoStates_tuple)
    D_forwarding_ifallsat, D_forwarding_sat, D_forwarding_unsat = arbiterModules.arbiterModule_reqsCheck(
        forwardDirections_tuple=D_forwardXYZ_target, directionStates_tuple=fifoStates_tuple)
    U_forwarding_ifallsat, U_forwarding_sat, U_forwarding_unsat = arbiterModules.arbiterModule_reqsCheck(
        forwardDirections_tuple=U_forwardXYZ_target, directionStates_tuple=fifoStates_tuple)

    # Arbiter Strategy - Fixed Priority IP-W-E-S-N-D-U
    if reqIP_tuple[0] and IP_forwarding_ifallsat:
        assert len(IP_forwarding_sat) == 1
        assert len(IP_forwarding_unsat) == 0
        forwards_tuple = copy.deepcopy(IP_forwardXYZ_target)
        grants_tuple = (True, False, False, False, False, False, False)
    elif reqW_tuple[0] and W_forwarding_ifallsat:
        assert len(W_forwarding_sat) == 1
        assert len(W_forwarding_unsat) == 0
        forwards_tuple = copy.deepcopy(W_forwardXYZ_target)
        grants_tuple = (False, True, False, False, False, False, False)
    elif reqE_tuple[0] and E_forwarding_ifallsat:
        assert len(E_forwarding_sat) == 1
        assert len(E_forwarding_unsat) == 0
        forwards_tuple = copy.deepcopy(E_forwardXYZ_target)
        grants_tuple = (False, False, True, False, False, False, False)
    elif reqS_tuple[0] and S_forwarding_ifallsat:
        assert len(S_forwarding_sat) == 1
        assert len(S_forwarding_unsat) == 0
        forwards_tuple = copy.deepcopy(S_forwardXYZ_target)
        grants_tuple = (False, False, False, True, False, False, False)
    elif reqN_tuple[0] and N_forwarding_ifallsat:
        assert len(N_forwarding_sat) == 1
        assert len(N_forwarding_unsat) == 0
        forwards_tuple = copy.deepcopy(N_forwardXYZ_target)
        grants_tuple = (False, False, False, False, True, False, False)
    elif reqD_tuple[0] and D_forwarding_ifallsat:
        assert len(D_forwarding_sat) == 1
        assert len(D_forwarding_unsat) == 0
        forwards_tuple = copy.deepcopy(D_forwardXYZ_target)
        grants_tuple = (False, False, False, False, False, True, False)
    elif reqU_tuple[0] and U_forwarding_ifallsat:
        assert len(U_forwarding_sat) == 1
        assert len(U_forwarding_unsat) == 0
        forwards_tuple = copy.deepcopy(U_forwardXYZ_target)
        grants_tuple = (False, False, False, False, False, False, True)
    else:
        forwards_tuple = (False, False, False, False, False, False, False)
        grants_tuple = (False, False, False, False, False, False, False)

    return (grants_tuple, forwards_tuple)