# The core logic of the Fixed Priority Arbiter with XOR-NC
import copy

import Arbiter_Logic.arbiterModules as arbiterModules

def arbiterNCLogic_fixedPriority(addrLocal_tuple, fifoStates_tuple, reqIP_tuple, reqW_tuple, reqE_tuple, reqS_tuple, reqN_tuple, reqD_tuple, reqU_tuple):
    '''
    The core logic of the Fixed Priority Arbiter with XOR-NC - Main \n
    grants_tuple: tuple(bool, bool, bool, bool, bool, bool, bool) - The reqs from (IP, W, E, S, N, D, U) will be processed. \n
    forwards_tuple: tuple(bool, bool, bool, bool, bool, bool, bool) - The forward directions are (IP, W, E, S, N, D, U).
    if_encoding: bool - If the granted packets should be encoded.

    :param addrLocal_tuple: tuple(int, int, int) - (addressX, addressY, addressZ)
    :param fifoStates_tuple: tuple(bool, bool, bool, bool, bool, bool, bool) - If the output fifos of (IP, W, E, S, N, D, U) has free space.
    :param reqIP_tuple: tuple(bool, int, int, int, int, int, int, bool) - (if_req_available, addressA-X, addressA-Y, addressA-Z, addressB-X, addressB-Y, addressB-Z, if_encodedPacket)
    :param reqW_tuple: tuple(bool, int, int, int, int, int, int, bool) - (if_req_available, addressA-X, addressA-Y, addressA-Z, addressB-X, addressB-Y, addressB-Z, if_encodedPacket)
    :param reqE_tuple: tuple(bool, int, int, int, int, int, int, bool) - (if_req_available, addressA-X, addressA-Y, addressA-Z, addressB-X, addressB-Y, addressB-Z, if_encodedPacket)
    :param reqS_tuple: tuple(bool, int, int, int, int, int, int, bool) - (if_req_available, addressA-X, addressA-Y, addressA-Z, addressB-X, addressB-Y, addressB-Z, if_encodedPacket)
    :param reqN_tuple: tuple(bool, int, int, int, int, int, int, bool) - (if_req_available, addressA-X, addressA-Y, addressA-Z, addressB-X, addressB-Y, addressB-Z, if_encodedPacket)
    :param reqD_tuple: tuple(bool, int, int, int, int, int, int, bool) - (if_req_available, addressA-X, addressA-Y, addressA-Z, addressB-X, addressB-Y, addressB-Z, if_encodedPacket)
    :param reqU_tuple: tuple(bool, int, int, int, int, int, int, bool) - (if_req_available, addressA-X, addressA-Y, addressA-Z, addressB-X, addressB-Y, addressB-Z, if_encodedPacket)
    :return: grants_tuple, forwards_tuple, if_performEncoding
    '''

    assert isinstance(addrLocal_tuple, tuple) and len(addrLocal_tuple) == 3
    assert isinstance(fifoStates_tuple, tuple) and len(fifoStates_tuple) == 7
    assert isinstance(reqIP_tuple, tuple) and len(reqIP_tuple) == 8
    assert isinstance(reqW_tuple, tuple) and len(reqW_tuple) == 8
    assert isinstance(reqE_tuple, tuple) and len(reqE_tuple) == 8
    assert isinstance(reqS_tuple, tuple) and len(reqS_tuple) == 8
    assert isinstance(reqN_tuple, tuple) and len(reqN_tuple) == 8
    assert isinstance(reqD_tuple, tuple) and len(reqD_tuple) == 8
    assert isinstance(reqU_tuple, tuple) and len(reqU_tuple) == 8

    # Compare addresses
    addrCompare_IP_A = arbiterModules.arbiterModule_addrCompare(addrLocal_tuple=addrLocal_tuple,
                                                              addrDes_tuple=reqIP_tuple[1:4])
    addrCompare_W_A = arbiterModules.arbiterModule_addrCompare(addrLocal_tuple=addrLocal_tuple,
                                                             addrDes_tuple=reqW_tuple[1:4])
    addrCompare_E_A = arbiterModules.arbiterModule_addrCompare(addrLocal_tuple=addrLocal_tuple,
                                                             addrDes_tuple=reqE_tuple[1:4])
    addrCompare_S_A = arbiterModules.arbiterModule_addrCompare(addrLocal_tuple=addrLocal_tuple,
                                                             addrDes_tuple=reqS_tuple[1:4])
    addrCompare_N_A = arbiterModules.arbiterModule_addrCompare(addrLocal_tuple=addrLocal_tuple,
                                                             addrDes_tuple=reqN_tuple[1:4])
    addrCompare_D_A = arbiterModules.arbiterModule_addrCompare(addrLocal_tuple=addrLocal_tuple,
                                                             addrDes_tuple=reqD_tuple[1:4])
    addrCompare_U_A = arbiterModules.arbiterModule_addrCompare(addrLocal_tuple=addrLocal_tuple,
                                                             addrDes_tuple=reqU_tuple[1:4])

    addrCompare_IP_B = arbiterModules.arbiterModule_addrCompare(addrLocal_tuple=addrLocal_tuple,
                                                                addrDes_tuple=reqIP_tuple[4:7])
    addrCompare_W_B = arbiterModules.arbiterModule_addrCompare(addrLocal_tuple=addrLocal_tuple,
                                                               addrDes_tuple=reqW_tuple[4:7])
    addrCompare_E_B = arbiterModules.arbiterModule_addrCompare(addrLocal_tuple=addrLocal_tuple,
                                                               addrDes_tuple=reqE_tuple[4:7])
    addrCompare_S_B = arbiterModules.arbiterModule_addrCompare(addrLocal_tuple=addrLocal_tuple,
                                                               addrDes_tuple=reqS_tuple[4:7])
    addrCompare_N_B = arbiterModules.arbiterModule_addrCompare(addrLocal_tuple=addrLocal_tuple,
                                                               addrDes_tuple=reqN_tuple[4:7])
    addrCompare_D_B = arbiterModules.arbiterModule_addrCompare(addrLocal_tuple=addrLocal_tuple,
                                                               addrDes_tuple=reqD_tuple[4:7])
    addrCompare_U_B = arbiterModules.arbiterModule_addrCompare(addrLocal_tuple=addrLocal_tuple,
                                                               addrDes_tuple=reqU_tuple[4:7])

    # Routing Mode 1: XYZ Routing ######################################################################################
    # XYZ Routing
    IP_forwardXYZ_target = arbiterModules.arbiterModule_routingAlg_XYZ(addrCompare_tuple=addrCompare_IP_A)
    W_forwardXYZ_target = arbiterModules.arbiterModule_routingAlg_XYZ(addrCompare_tuple=addrCompare_W_A)
    E_forwardXYZ_target = arbiterModules.arbiterModule_routingAlg_XYZ(addrCompare_tuple=addrCompare_E_A)
    S_forwardXYZ_target = arbiterModules.arbiterModule_routingAlg_XYZ(addrCompare_tuple=addrCompare_S_A)
    N_forwardXYZ_target = arbiterModules.arbiterModule_routingAlg_XYZ(addrCompare_tuple=addrCompare_N_A)
    D_forwardXYZ_target = arbiterModules.arbiterModule_routingAlg_XYZ(addrCompare_tuple=addrCompare_D_A)
    U_forwardXYZ_target = arbiterModules.arbiterModule_routingAlg_XYZ(addrCompare_tuple=addrCompare_U_A)

    # Forwarding directions check
    IP_forwardXYZ_ifallsat, IP_forwardXYZ_sat, IP_forwardXYZ_unsat = arbiterModules.arbiterModule_reqsCheck(
        forwardDirections_tuple=IP_forwardXYZ_target, directionStates_tuple=fifoStates_tuple)
    W_forwardXYZ_ifallsat, W_forwardXYZ_sat, W_forwardXYZ_unsat = arbiterModules.arbiterModule_reqsCheck(
        forwardDirections_tuple=W_forwardXYZ_target, directionStates_tuple=fifoStates_tuple)
    E_forwardXYZ_ifallsat, E_forwardXYZ_sat, E_forwardXYZ_unsat = arbiterModules.arbiterModule_reqsCheck(
        forwardDirections_tuple=E_forwardXYZ_target, directionStates_tuple=fifoStates_tuple)
    S_forwardXYZ_ifallsat, S_forwardXYZ_sat, S_forwardXYZ_unsat = arbiterModules.arbiterModule_reqsCheck(
        forwardDirections_tuple=S_forwardXYZ_target, directionStates_tuple=fifoStates_tuple)
    N_forwardXYZ_ifallsat, N_forwardXYZ_sat, N_forwardXYZ_unsat = arbiterModules.arbiterModule_reqsCheck(
        forwardDirections_tuple=N_forwardXYZ_target, directionStates_tuple=fifoStates_tuple)
    D_forwardXYZ_ifallsat, D_forwardXYZ_sat, D_forwardXYZ_unsat = arbiterModules.arbiterModule_reqsCheck(
        forwardDirections_tuple=D_forwardXYZ_target, directionStates_tuple=fifoStates_tuple)
    U_forwardXYZ_ifallsat, U_forwardXYZ_sat, U_forwardXYZ_unsat = arbiterModules.arbiterModule_reqsCheck(
        forwardDirections_tuple=U_forwardXYZ_target, directionStates_tuple=fifoStates_tuple)

    # Routing Mode 2: Routing for Encoded Packet #######################################################################
    # Routing for encoded packets
    W_forwardEncoded_target = arbiterModules.arbiterNCModule_routingAlg_EncodedWIn(addrCompare_tupleA=addrCompare_W_A,
                                                                                   addrCompare_tupleB=addrCompare_W_B)
    E_forwardEncoded_target = arbiterModules.arbiterNCModule_routingAlg_EncodedEIn(addrCompare_tupleA=addrCompare_E_A,
                                                                                   addrCompare_tupleB=addrCompare_E_B)
    S_forwardEncoded_target = arbiterModules.arbiterNCModule_routingAlg_EncodedSIn(addrCompare_tupleA=addrCompare_S_A,
                                                                                   addrCompare_tupleB=addrCompare_S_B)
    N_forwardEncoded_target = arbiterModules.arbiterNCModule_routingAlg_EncodedNIn(addrCompare_tupleA=addrCompare_N_A,
                                                                                   addrCompare_tupleB=addrCompare_N_B)
    D_forwardEncoded_target = arbiterModules.arbiterNCModule_routingAlg_EncodedDIn(addrCompare_tupleA=addrCompare_D_A,
                                                                                   addrCompare_tupleB=addrCompare_D_B)
    U_forwardEncoded_target = arbiterModules.arbiterNCModule_routingAlg_EncodedUIn(addrCompare_tupleA=addrCompare_U_A,
                                                                                   addrCompare_tupleB=addrCompare_U_B)

    # Forwarding direction check
    W_forwardEncoded_ifallsat, W_forwardEncoded_sat, W_forwardEncoded_unsat = arbiterModules.arbiterModule_reqsCheck(
        forwardDirections_tuple=W_forwardEncoded_target, directionStates_tuple=fifoStates_tuple)
    E_forwardEncoded_ifallsat, E_forwardEncoded_sat, E_forwardEncoded_unsat = arbiterModules.arbiterModule_reqsCheck(
        forwardDirections_tuple=E_forwardEncoded_target, directionStates_tuple=fifoStates_tuple)
    S_forwardEncoded_ifallsat, S_forwardEncoded_sat, S_forwardEncoded_unsat = arbiterModules.arbiterModule_reqsCheck(
        forwardDirections_tuple=S_forwardEncoded_target, directionStates_tuple=fifoStates_tuple)
    N_forwardEncoded_ifallsat, N_forwardEncoded_sat, N_forwardEncoded_unsat = arbiterModules.arbiterModule_reqsCheck(
        forwardDirections_tuple=N_forwardEncoded_target, directionStates_tuple=fifoStates_tuple)
    D_forwardEncoded_ifallsat, D_forwardEncoded_sat, D_forwardEncoded_unsat = arbiterModules.arbiterModule_reqsCheck(
        forwardDirections_tuple=D_forwardEncoded_target, directionStates_tuple=fifoStates_tuple)
    U_forwardEncoded_ifallsat, U_forwardEncoded_sat, U_forwardEncoded_unsat = arbiterModules.arbiterModule_reqsCheck(
        forwardDirections_tuple=U_forwardEncoded_target, directionStates_tuple=fifoStates_tuple)

    # Routing Mode 3: Performing XOR-NC encoding and forwarding the encoded packet #####################################
    # Encoding rules
    WE_encoding_ifEncoding, WE_encodingFw_target = arbiterModules.arbiterNCModule_NCEncodingRules_WE(addrCompare_tuple01=addrCompare_W_A, addrCompare_tuple02=addrCompare_E_A)
    NS_encoding_ifEncoding, NS_encodingFw_target = arbiterModules.arbiterNCModule_NCEncodingRules_NS(addrCompare_tuple01=addrCompare_N_A, addrCompare_tuple02=addrCompare_S_A)

    # Forwarding direction check
    WE_encodingFw_ifallsat, WE_encodingFw_sat, WE_encodingFw_unsat = arbiterModules.arbiterModule_reqsCheck(
        forwardDirections_tuple=WE_encodingFw_target, directionStates_tuple=fifoStates_tuple)
    NS_encodingFw_ifallsat, NS_encodingFw_sat, NS_encodingFw_unsat = arbiterModules.arbiterModule_reqsCheck(
        forwardDirections_tuple=NS_encodingFw_target, directionStates_tuple=fifoStates_tuple)

    ####################################################################################################################
    # Arbiter - Main ###################################################################################################
    # Encoding WE
    if WE_encoding_ifEncoding and WE_encodingFw_ifallsat and reqW_tuple[0] and reqE_tuple[0] and (not reqW_tuple[7]) and (not reqE_tuple[7]):
        grants_tuple = (False, True, True, False, False, False, False)
        forward_tuple = copy.deepcopy(WE_encodingFw_target)
        if_performingEncoding = True
    # Encoding NS
    elif NS_encoding_ifEncoding and NS_encodingFw_ifallsat and reqN_tuple[0] and reqS_tuple[0] and (not reqN_tuple[7]) and (not reqS_tuple[7]):
        grants_tuple = (False, False, False, True, True, False, False)
        forward_tuple = opy.deepcopy(NS_encodingFw_target)
        if_performingEncoding = True
    # IP - XYZ
    elif reqIP_tuple[0] and IP_forwardXYZ_ifallsat:
        assert not reqIP_tuple[7]
        grants_tuple = (True, False, False, False, False, False, False)
        forward_tuple = copy.deepcopy(IP_forwardXYZ_target)
        if_performingEncoding = False
    # W - Encoded
    elif reqW_tuple[0] and W_forwardEncoded_ifallsat and reqW_tuple[7]:
        grants_tuple = (False, True, False, False, False, False, False)
        forward_tuple = copy.deepcopy(W_forwardEncoded_target)
        if_performingEncoding = False
    # W - XYZ
    elif reqW_tuple[0] and W_forwardXYZ_ifallsat and (not reqW_tuple[7]):
        grants_tuple = (False, True, False, False, False, False, False)
        forward_tuple = copy.deepcopy(W_forwardXYZ_target)
        if_performingEncoding = False
    # E - Encoded
    elif reqE_tuple[0] and E_forwardEncoded_ifallsat and reqE_tuple[7]:
        grants_tuple = (False, False, True, False, False, False, False)
        forward_tuple = copy.deepcopy(E_forwardEncoded_target)
        if_performingEncoding = False
    # E - XYZ
    elif reqE_tuple[0] and E_forwardXYZ_ifallsat and (not reqE_tuple[7]):
        grants_tuple = (False, False, True, False, False, False, False)
        forward_tuple = copy.deepcopy(E_forwardXYZ_target)
        if_performingEncoding = False
    # S - Encoded
    elif reqS_tuple[0] and S_forwardEncoded_ifallsat and reqS_tuple[7]:
        grants_tuple = (False, False, False, True, False, False, False)
        forward_tuple = copy.deepcopy(S_forwardEncoded_target)
        if_performingEncoding = False
    # S - XYZ
    elif reqS_tuple[0] and S_forwardXYZ_ifallsat and (not reqS_tuple[7]):
        grants_tuple = (False, False, False, True, False, False, False)
        forward_tuple = copy.deepcopy(S_forwardXYZ_target)
        if_performingEncoding = False
    # N - Encoded
    elif reqN_tuple[0] and N_forwardEncoded_ifallsat and reqN_tuple[7]:
        grants_tuple = (False, False, False, False, True, False, False)
        forward_tuple = copy.deepcopy(N_forwardEncoded_target)
        if_performingEncoding = False
    # N - XYZ
    elif reqN_tuple[0] and N_forwardXYZ_ifallsat and (not reqN_tuple[7]):
        grants_tuple = (False, False, False, False, True, False, False)
        forward_tuple = copy.deepcopy(N_forwardXYZ_target)
        if_performingEncoding = False
    # D - Encoded
    elif reqD_tuple[0] and D_forwardEncoded_ifallsat and reqD_tuple[7]:
        grants_tuple = (False, False, False, False, False, True, False)
        forward_tuple = copy.deepcopy(D_forwardEncoded_target)
        if_performingEncoding = False
    # D - XYZ
    elif reqD_tuple[0] and D_forwardXYZ_ifallsat and (not reqD_tuple[7]):
        grants_tuple = (False, False, False, False, False, True, False)
        forward_tuple = copy.deepcopy(D_forwardXYZ_target)
        if_performingEncoding = False
    # U - Encoded
    elif reqU_tuple[0] and U_forwardEncoded_ifallsat and reqU_tuple[7]:
        grants_tuple = (False, False, False, False, False, False, True)
        forward_tuple = copy.deepcopy(U_forwardEncoded_target)
        if_performingEncoding = False
    # U - XYZ
    elif reqU_tuple[0] and U_forwardXYZ_ifallsat and (not reqU_tuple[7]):
        grants_tuple = (False, False, False, False, False, False, True)
        forward_tuple = copy.deepcopy(U_forwardXYZ_target)
        if_performingEncoding = False
    # No req can be processed
    else:
        grants_tuple = (False, False, False, False, False, False, False)
        forward_tuple = (False, False, False, False, False, False, False)
        if_performingEncoding = False

    return grants_tuple, forward_tuple, if_performingEncoding