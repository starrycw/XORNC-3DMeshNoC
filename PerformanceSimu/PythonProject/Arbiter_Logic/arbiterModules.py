# Modules of arbiter
import copy


########################################################################################################################
########################################################################################################################
def arbiterModule_addrCompare(addrLocal_tuple, addrDes_tuple):
    '''
    Compare the local address and the destination address in a req. Return a tuple (\n
    [0 bool]-if the destination address is same as the local address (des is IP),\n
    [1 bool]-if the destination address X > the local address X (des locates at E),\n
    [2 bool]-if the destination address X < the local address X (des locates at W),\n
    [3 bool]-if the destination address Y > the local address Y (des locates at N),\n
    [4 bool]-if the destination address Y < the local address Y (des locates at S),\n
    [5 bool]-if the destination address Z > the local address Z (des locates at U),\n
    [6 bool]-if the destination address Z < the local address Z (des locates at D),\n
    )

    :param addrLocal_tuple: tuple(int, int, int) - (addressX, addressY, addressZ)
    :param addrDes_tuple: tuple(int, int, int) - (addressX, addressY, addressZ)
    :return: addrDiff: tuple(bool, bool, bool, bool, bool, bool, bool)
    '''

    assert isinstance(addrLocal_tuple, tuple) and len(addrLocal_tuple) == 3
    assert isinstance(addrDes_tuple, tuple) and len(addrDes_tuple) == 3

    addrDiff_list = []
    if_addrEqual = True
    for idx_i in range(0, 3):
        if addrDes_tuple[idx_i] > addrLocal_tuple[idx_i]:
            addrDiff_list.append(True)
            addrDiff_list.append(False)
            if_addrEqual = False
        elif addrDes_tuple[idx_i] < addrLocal_tuple[idx_i]:
            addrDiff_list.append(False)
            addrDiff_list.append(True)
            if_addrEqual = False
        else:
            addrDiff_list.append(False)
            addrDiff_list.append(False)

    # Return
    assert len(addrDiff_list) == 6
    addrDiff = (if_addrEqual, addrDiff_list[0], addrDiff_list[1], addrDiff_list[2], addrDiff_list[3], addrDiff_list[4], addrDiff_list[5])
    assert not (addrDiff[1] and addrDiff[2])
    assert not (addrDiff[3] and addrDiff[4])
    assert not (addrDiff[5] and addrDiff[6])
    return addrDiff
########################################################################################################################
########################################################################################################################


def arbiterModule_routingAlg_XYZ(addrCompare_tuple):
    '''
    XYZ-DOR
    
    :param addrCompare_tuple: tuple(bool, bool, bool, bool, bool, bool, bool) - See the return param of function arbiterModule_addrCompare.
    :return: tuple(bool, bool, bool, bool, bool, bool, bool) - The packets should be forwarded to port (IP, W, E, S, N, D, U). Note that ONLY ONE element of this tuple is True!
    '''
    assert isinstance(addrCompare_tuple, tuple) and len(addrCompare_tuple) == 7
    if addrCompare_tuple[0]:
        assert not (addrCompare_tuple[1] or addrCompare_tuple[2] or addrCompare_tuple[3] or addrCompare_tuple[4] or addrCompare_tuple[5] or addrCompare_tuple[6])
        return (True, False, False, False, False, False, False)
    elif addrCompare_tuple[2]:
        assert not (addrCompare_tuple[0] or addrCompare_tuple[1])
        return (False, True, False, False, False, False, False)
    elif addrCompare_tuple[1]:
        assert not (addrCompare_tuple[0] or addrCompare_tuple[2])
        return (False, False, True, False, False, False, False)
    elif addrCompare_tuple[4]:
        assert not (addrCompare_tuple[0] or addrCompare_tuple[1] or addrCompare_tuple[2] or addrCompare_tuple[3])
        return (False, False, False, True, False, False, False)
    elif addrCompare_tuple[3]:
        assert not (addrCompare_tuple[0] or addrCompare_tuple[1] or addrCompare_tuple[2] or addrCompare_tuple[4])
        return (False, False, False, False, True, False, False)
    elif addrCompare_tuple[6]:
        assert not (addrCompare_tuple[0] or addrCompare_tuple[1] or addrCompare_tuple[2] or addrCompare_tuple[3] or addrCompare_tuple[4] or addrCompare_tuple[5])
        return (False, False, False, False, False, True, False)
    elif addrCompare_tuple[5]:
        assert not (addrCompare_tuple[0] or addrCompare_tuple[1] or addrCompare_tuple[2] or addrCompare_tuple[3] or addrCompare_tuple[4] or addrCompare_tuple[6])
        return (False, False, False, False, False, False, True)
    else:
        assert False
########################################################################################################################
########################################################################################################################


def arbiterModule_reqsCheck(forwardDirections_tuple, directionStates_tuple):
    '''
    Check if the forwarding destination are available. \n
            if_allSat: bool - if all the forwarding directions are available \n
            tuple(forwardingAvailable_list): tuple - The available forwarding directions \n
            tuple(forwardingUnsat_list): tuple - The forwarding directions with unavailable fifo state

    :param forwardDirections_tuple: tuple(bool, bool, ...) - The forwarding directions
    :param directionStates_tuple: tuple(bool, bool, ...) - The fifo states of the output ports at corresponding directions
    :return: if_allSat, tuple(forwardingAvailable_list), tuple(forwardingUnsat_list)
    '''
    assert isinstance(forwardDirections_tuple, tuple)
    assert isinstance(directionStates_tuple, tuple)
    assert len(forwardDirections_tuple) == len(directionStates_tuple)
    if_allSat = True
    forwardingAvailable_list = []
    forwardingUnsat_list = []
    for idx_i in range(0, len(forwardDirections_tuple)):
        if forwardDirections_tuple[idx_i] is True:
            if directionStates_tuple[idx_i] is True:
                forwardingAvailable_list.append(idx_i)
            elif directionStates_tuple[idx_i] is False:
                if_allSat = False
                forwardingUnsat_list.append(idx_i)
            else:
                assert False
    return if_allSat, tuple(forwardingAvailable_list), tuple(forwardingUnsat_list)
########################################################################################################################
########################################################################################################################


def arbiterNCModule_routingAlg_EncodedWIn(addrCompare_tupleA, addrCompare_tupleB):
    '''
    The routing alg for the encoded packets input from the W port.

    :param addrCompare_tupleA: tuple(bool, bool, bool, bool, bool, bool, bool) - See the return param of function arbiterModule_addrCompare.
    :param addrCompare_tupleB: tuple(bool, bool, bool, bool, bool, bool, bool) - See the return param of function arbiterModule_addrCompare.
    :return: tuple(bool, bool, bool, bool, bool, bool, bool) - The packets should be forwarded to ports (IP, W, E, S, N, D, U).
    '''
    assert isinstance(addrCompare_tupleA, tuple) and len(addrCompare_tupleA) == 7
    assert isinstance(addrCompare_tupleB, tuple) and len(addrCompare_tupleB) == 7
    fwTarget_list = [False, False, False, False, False, False, False]
    if addrCompare_tupleA[0] or addrCompare_tupleB[0]:
        fwTarget_list[0] = True
    if addrCompare_tupleA[1] and (not addrCompare_tupleA[3]) and (not addrCompare_tupleA[4]) and (not addrCompare_tupleA[5]) and (not addrCompare_tupleA[6]):
        fwTarget_list[2] = True
    if addrCompare_tupleB[1] and (not addrCompare_tupleB[3]) and (not addrCompare_tupleB[4]) and (not addrCompare_tupleB[5]) and (not addrCompare_tupleB[6]):
        fwTarget_list[2] = True
    return tuple(fwTarget_list)
########################################################################################################################
########################################################################################################################


def arbiterNCModule_routingAlg_EncodedEIn(addrCompare_tupleA, addrCompare_tupleB):
    '''
    The routing alg for the encoded packets input from the E port.

    :param addrCompare_tupleA: tuple(bool, bool, bool, bool, bool, bool, bool) - See the return param of function arbiterModule_addrCompare.
    :param addrCompare_tupleB: tuple(bool, bool, bool, bool, bool, bool, bool) - See the return param of function arbiterModule_addrCompare.
    :return: tuple(bool, bool, bool, bool, bool, bool, bool) - The packets should be forwarded to ports (IP, W, E, S, N, D, U).
    '''
    assert isinstance(addrCompare_tupleA, tuple) and len(addrCompare_tupleA) == 7
    assert isinstance(addrCompare_tupleB, tuple) and len(addrCompare_tupleB) == 7
    fwTarget_list = [False, False, False, False, False, False, False]
    if addrCompare_tupleA[0] or addrCompare_tupleB[0]:
        fwTarget_list[0] = True
    if addrCompare_tupleA[2] and (not addrCompare_tupleA[3]) and (not addrCompare_tupleA[4]) and (not addrCompare_tupleA[5]) and (not addrCompare_tupleA[6]):
        fwTarget_list[1] = True
    if addrCompare_tupleB[2] and (not addrCompare_tupleB[3]) and (not addrCompare_tupleB[4]) and (not addrCompare_tupleB[5]) and (not addrCompare_tupleB[6]):
        fwTarget_list[1] = True
    return tuple(fwTarget_list)
########################################################################################################################
########################################################################################################################


def arbiterNCModule_routingAlg_EncodedSIn(addrCompare_tupleA, addrCompare_tupleB):
    '''
    The routing alg for the encoded packets input from the S port.

    :param addrCompare_tupleA: tuple(bool, bool, bool, bool, bool, bool, bool) - See the return param of function arbiterModule_addrCompare.
    :param addrCompare_tupleB: tuple(bool, bool, bool, bool, bool, bool, bool) - See the return param of function arbiterModule_addrCompare.
    :return: tuple(bool, bool, bool, bool, bool, bool, bool) - The packets should be forwarded to ports (IP, W, E, S, N, D, U).
    '''
    assert isinstance(addrCompare_tupleA, tuple) and len(addrCompare_tupleA) == 7
    assert isinstance(addrCompare_tupleB, tuple) and len(addrCompare_tupleB) == 7
    fwTarget_list = [False, False, False, False, False, False, False]
    # IP
    if addrCompare_tupleA[0] or addrCompare_tupleB[0]:
        fwTarget_list[0] = True
    # W
    if addrCompare_tupleA[2] and (not addrCompare_tupleA[3]) and (not addrCompare_tupleA[4]) and (not addrCompare_tupleA[5]) and (not addrCompare_tupleA[6]):
        fwTarget_list[1] = True
    if addrCompare_tupleB[2] and (not addrCompare_tupleB[3]) and (not addrCompare_tupleB[4]) and (not addrCompare_tupleB[5]) and (not addrCompare_tupleB[6]):
        fwTarget_list[1] = True
    # E
    if addrCompare_tupleA[1] and (not addrCompare_tupleA[3]) and (not addrCompare_tupleA[4]) and (not addrCompare_tupleA[5]) and (not addrCompare_tupleA[6]):
        fwTarget_list[2] = True
    if addrCompare_tupleB[1] and (not addrCompare_tupleB[3]) and (not addrCompare_tupleB[4]) and (not addrCompare_tupleB[5]) and (not addrCompare_tupleB[6]):
        fwTarget_list[2] = True
    # N
    if addrCompare_tupleA[3] or addrCompare_tupleB[3]:
        fwTarget_list[4] = True
    # U
    if (not addrCompare_tupleA[3]) and (not addrCompare_tupleA[4]) and addrCompare_tupleA[5]:
        fwTarget_list[6] = True
    if (not addrCompare_tupleB[3]) and (not addrCompare_tupleB[4]) and addrCompare_tupleB[5]:
        fwTarget_list[6] = True
    # D
    if (not addrCompare_tupleA[3]) and (not addrCompare_tupleA[4]) and addrCompare_tupleA[6]:
        fwTarget_list[5] = True
    if (not addrCompare_tupleB[3]) and (not addrCompare_tupleB[4]) and addrCompare_tupleB[6]:
        fwTarget_list[5] = True
    return tuple(fwTarget_list)
########################################################################################################################
########################################################################################################################


def arbiterNCModule_routingAlg_EncodedNIn(addrCompare_tupleA, addrCompare_tupleB):
    '''
    The routing alg for the encoded packets input from the N port.

    :param addrCompare_tupleA: tuple(bool, bool, bool, bool, bool, bool, bool) - See the return param of function arbiterModule_addrCompare.
    :param addrCompare_tupleB: tuple(bool, bool, bool, bool, bool, bool, bool) - See the return param of function arbiterModule_addrCompare.
    :return: tuple(bool, bool, bool, bool, bool, bool, bool) - The packets should be forwarded to ports (IP, W, E, S, N, D, U).
    '''
    assert isinstance(addrCompare_tupleA, tuple) and len(addrCompare_tupleA) == 7
    assert isinstance(addrCompare_tupleB, tuple) and len(addrCompare_tupleB) == 7
    fwTarget_list = [False, False, False, False, False, False, False]
    # IP
    if addrCompare_tupleA[0] or addrCompare_tupleB[0]:
        fwTarget_list[0] = True
    # W
    if addrCompare_tupleA[2] and (not addrCompare_tupleA[3]) and (not addrCompare_tupleA[4]) and (not addrCompare_tupleA[5]) and (not addrCompare_tupleA[6]):
        fwTarget_list[1] = True
    if addrCompare_tupleB[2] and (not addrCompare_tupleB[3]) and (not addrCompare_tupleB[4]) and (not addrCompare_tupleB[5]) and (not addrCompare_tupleB[6]):
        fwTarget_list[1] = True
    # E
    if addrCompare_tupleA[1] and (not addrCompare_tupleA[3]) and (not addrCompare_tupleA[4]) and (not addrCompare_tupleA[5]) and (not addrCompare_tupleA[6]):
        fwTarget_list[2] = True
    if addrCompare_tupleB[1] and (not addrCompare_tupleB[3]) and (not addrCompare_tupleB[4]) and (not addrCompare_tupleB[5]) and (not addrCompare_tupleB[6]):
        fwTarget_list[2] = True
    # S
    if addrCompare_tupleA[4] or addrCompare_tupleB[4]:
        fwTarget_list[3] = True
    # U
    if (not addrCompare_tupleA[3]) and (not addrCompare_tupleA[4]) and addrCompare_tupleA[5]:
        fwTarget_list[6] = True
    if (not addrCompare_tupleB[3]) and (not addrCompare_tupleB[4]) and addrCompare_tupleB[5]:
        fwTarget_list[6] = True
    # D
    if (not addrCompare_tupleA[3]) and (not addrCompare_tupleA[4]) and addrCompare_tupleA[6]:
        fwTarget_list[5] = True
    if (not addrCompare_tupleB[3]) and (not addrCompare_tupleB[4]) and addrCompare_tupleB[6]:
        fwTarget_list[5] = True
    return tuple(fwTarget_list)
########################################################################################################################
########################################################################################################################


def arbiterNCModule_routingAlg_EncodedDIn(addrCompare_tupleA, addrCompare_tupleB):
    '''
    The routing alg for the encoded packets input from the D port.

    :param addrCompare_tupleA: tuple(bool, bool, bool, bool, bool, bool, bool) - See the return param of function arbiterModule_addrCompare.
    :param addrCompare_tupleB: tuple(bool, bool, bool, bool, bool, bool, bool) - See the return param of function arbiterModule_addrCompare.
    :return: tuple(bool, bool, bool, bool, bool, bool, bool) - The packets should be forwarded to ports (IP, W, E, S, N, D, U).
    '''
    assert isinstance(addrCompare_tupleA, tuple) and len(addrCompare_tupleA) == 7
    assert isinstance(addrCompare_tupleB, tuple) and len(addrCompare_tupleB) == 7
    fwTarget_list = [False, False, False, False, False, False, False]
    # IP
    if addrCompare_tupleA[0] or addrCompare_tupleB[0]:
        fwTarget_list[0] = True
    # W
    if addrCompare_tupleA[2] and (not addrCompare_tupleA[3]) and (not addrCompare_tupleA[4]) and (not addrCompare_tupleA[5]) and (not addrCompare_tupleA[6]):
        fwTarget_list[1] = True
    if addrCompare_tupleB[2] and (not addrCompare_tupleB[3]) and (not addrCompare_tupleB[4]) and (not addrCompare_tupleB[5]) and (not addrCompare_tupleB[6]):
        fwTarget_list[1] = True
    # E
    if addrCompare_tupleA[1] and (not addrCompare_tupleA[3]) and (not addrCompare_tupleA[4]) and (not addrCompare_tupleA[5]) and (not addrCompare_tupleA[6]):
        fwTarget_list[2] = True
    if addrCompare_tupleB[1] and (not addrCompare_tupleB[3]) and (not addrCompare_tupleB[4]) and (not addrCompare_tupleB[5]) and (not addrCompare_tupleB[6]):
        fwTarget_list[2] = True
    # S
    if (not addrCompare_tupleA[5]) and (not addrCompare_tupleA[6]) and addrCompare_tupleA[4] and addrCompare_tupleB[3]:
        fwTarget_list[3] = True
    if (not addrCompare_tupleB[5]) and (not addrCompare_tupleB[6]) and addrCompare_tupleB[4] and addrCompare_tupleA[3]:
        fwTarget_list[3] = True
    # N
    if (not addrCompare_tupleA[5]) and (not addrCompare_tupleA[6]) and addrCompare_tupleA[3] and addrCompare_tupleB[4]:
        fwTarget_list[4] = True
    if (not addrCompare_tupleB[5]) and (not addrCompare_tupleB[6]) and addrCompare_tupleB[3] and addrCompare_tupleA[4]:
        fwTarget_list[4] = True
    # U
    if addrCompare_tupleA[5] or addrCompare_tupleB[5]:
        fwTarget_list[6] = True

    # NS-Additional
    if fwTarget_list == [False, False, False, False, False, False, False]:
        if (not addrCompare_tupleA[5]) and (not addrCompare_tupleA[6]) and addrCompare_tupleA[4]:
            fwTarget_list[3] = True
        if (not addrCompare_tupleB[5]) and (not addrCompare_tupleB[6]) and addrCompare_tupleB[4]:
            fwTarget_list[3] = True

        if (not addrCompare_tupleA[5]) and (not addrCompare_tupleA[6]) and addrCompare_tupleA[3]:
            fwTarget_list[4] = True
        if (not addrCompare_tupleB[5]) and (not addrCompare_tupleB[6]) and addrCompare_tupleB[3]:
            fwTarget_list[4] = True


    return tuple(fwTarget_list)
########################################################################################################################
########################################################################################################################


def arbiterNCModule_routingAlg_EncodedUIn(addrCompare_tupleA, addrCompare_tupleB):
    '''
    The routing alg for the encoded packets input from the U port.

    :param addrCompare_tupleA: tuple(bool, bool, bool, bool, bool, bool, bool) - See the return param of function arbiterModule_addrCompare.
    :param addrCompare_tupleB: tuple(bool, bool, bool, bool, bool, bool, bool) - See the return param of function arbiterModule_addrCompare.
    :return: tuple(bool, bool, bool, bool, bool, bool, bool) - The packets should be forwarded to ports (IP, W, E, S, N, D, U).
    '''
    assert isinstance(addrCompare_tupleA, tuple) and len(addrCompare_tupleA) == 7
    assert isinstance(addrCompare_tupleB, tuple) and len(addrCompare_tupleB) == 7
    fwTarget_list = [False, False, False, False, False, False, False]
    # IP
    if addrCompare_tupleA[0] or addrCompare_tupleB[0]:
        fwTarget_list[0] = True
    # W
    if addrCompare_tupleA[2] and (not addrCompare_tupleA[3]) and (not addrCompare_tupleA[4]) and (not addrCompare_tupleA[5]) and (not addrCompare_tupleA[6]):
        fwTarget_list[1] = True
    if addrCompare_tupleB[2] and (not addrCompare_tupleB[3]) and (not addrCompare_tupleB[4]) and (not addrCompare_tupleB[5]) and (not addrCompare_tupleB[6]):
        fwTarget_list[1] = True
    # E
    if addrCompare_tupleA[1] and (not addrCompare_tupleA[3]) and (not addrCompare_tupleA[4]) and (not addrCompare_tupleA[5]) and (not addrCompare_tupleA[6]):
        fwTarget_list[2] = True
    if addrCompare_tupleB[1] and (not addrCompare_tupleB[3]) and (not addrCompare_tupleB[4]) and (not addrCompare_tupleB[5]) and (not addrCompare_tupleB[6]):
        fwTarget_list[2] = True
    # S
    if (not addrCompare_tupleA[5]) and (not addrCompare_tupleA[6]) and addrCompare_tupleA[4] and addrCompare_tupleB[3]:
        fwTarget_list[3] = True
    if (not addrCompare_tupleB[5]) and (not addrCompare_tupleB[6]) and addrCompare_tupleB[4] and addrCompare_tupleA[3]:
        fwTarget_list[3] = True
    # N
    if (not addrCompare_tupleA[5]) and (not addrCompare_tupleA[6]) and addrCompare_tupleA[3] and addrCompare_tupleB[4]:
        fwTarget_list[4] = True
    if (not addrCompare_tupleB[5]) and (not addrCompare_tupleB[6]) and addrCompare_tupleB[3] and addrCompare_tupleA[4]:
        fwTarget_list[4] = True
    # D
    if addrCompare_tupleA[6] or addrCompare_tupleB[6]:
        fwTarget_list[5] = True

    # NS-Additional
    if fwTarget_list == [False, False, False, False, False, False, False]:
        if (not addrCompare_tupleA[5]) and (not addrCompare_tupleA[6]) and addrCompare_tupleA[4]:
            fwTarget_list[3] = True
        if (not addrCompare_tupleB[5]) and (not addrCompare_tupleB[6]) and addrCompare_tupleB[4]:
            fwTarget_list[3] = True

        if (not addrCompare_tupleA[5]) and (not addrCompare_tupleA[6]) and addrCompare_tupleA[3]:
            fwTarget_list[4] = True
        if (not addrCompare_tupleB[5]) and (not addrCompare_tupleB[6]) and addrCompare_tupleB[3]:
            fwTarget_list[4] = True

    return tuple(fwTarget_list)
########################################################################################################################
########################################################################################################################


def arbiterNCModule_NCEncodingRules_WE(addrCompare_tuple01, addrCompare_tuple02):
    '''
    The strategy for encoding the packets from W and E ports.\n
    if_encoding - bool - If these two packets should be encoded.\n
    fwTarget_tuple - tuple(bool, bool, bool, bool, bool, bool, bool) - The packets should be forwarded to ports (IP, W, E, S, N, D, U).

    :param addrCompare_tuple01: tuple(bool, bool, bool, bool, bool, bool, bool) - See the return param of function arbiterModule_addrCompare.
    :param addrCompare_tuple02: tuple(bool, bool, bool, bool, bool, bool, bool) - See the return param of function arbiterModule_addrCompare.
    :return: if_encoding, fwTarget_tuple
    '''
    addrCompare_tupleA = copy.deepcopy(addrCompare_tuple01)
    addrCompare_tupleB = copy.deepcopy(addrCompare_tuple02)
    assert isinstance(addrCompare_tupleA, tuple) and len(addrCompare_tupleA) == 7
    assert isinstance(addrCompare_tupleB, tuple) and len(addrCompare_tupleB) == 7

    # Condition A: Two destinations locate at the same XY plane as the local router
    cA_ifSat_c1 = False  # redundant. cA_ifSat_C1 is expected to be True.
    cA_ifSat = False
    if (not addrCompare_tupleA[1]) and (not addrCompare_tupleB[2]): #
        cA_ifSat_c1 = True #
    if (not addrCompare_tupleA[2]) and (not addrCompare_tupleB[1]): #
        cA_ifSat_c1 = True #
    # assert cA_ifSat_c1 #
    if addrCompare_tupleA[3] and addrCompare_tupleB[3]:
        cA_ifSat = True
    if addrCompare_tupleA[4] and addrCompare_tupleB[4]:
        cA_ifSat = True

    # Condition B: Two destinations locate at the same XZ plane as the local router.
    cB_ifSat_c1 = False  # redundant. cB_ifSat_C1 is expected to be True.
    cB_ifSat = False
    if (not addrCompare_tupleA[1]) and (not addrCompare_tupleB[2]):  #
        cB_ifSat_c1 = True  #
    if (not addrCompare_tupleA[2]) and (not addrCompare_tupleB[1]):  #
        cB_ifSat_c1 = True  #
    # assert cB_ifSat_c1  #
    if addrCompare_tupleA[5] and addrCompare_tupleB[5]:
        cB_ifSat = True
    if addrCompare_tupleA[6] and addrCompare_tupleB[6]:
        cB_ifSat = True

    # Condition C and D: Not all the destinations locate at the same plane as the local router.
    cC_ifSat = False
    cD_ifSat = False
    if (addrCompare_tupleA[1] or addrCompare_tupleA[2] or addrCompare_tupleB[1] or addrCompare_tupleB[2]) and (addrCompare_tupleA[3] or addrCompare_tupleA[4] or addrCompare_tupleB[3] or addrCompare_tupleB[4]) and (addrCompare_tupleA[5] or addrCompare_tupleA[6] or addrCompare_tupleB[5] or addrCompare_tupleB[6]):
        # Condition C: Take the XZ plane as the reference plane of sources. Not all the destinations locate at the same plane as the local router.
        if (not addrCompare_tupleA[3]) and (not addrCompare_tupleB[3]):
            cC_ifSat = True
        if (not addrCompare_tupleA[4]) and (not addrCompare_tupleB[4]):
            cC_ifSat = True
        # Condition D: Take the XY plane as the reference plane of sources. Not all the destinations locate at the same plane as the local router.
        if (not addrCompare_tupleA[5]) and (not addrCompare_tupleB[5]):
            cD_ifSat = True
        if (not addrCompare_tupleA[6]) and (not addrCompare_tupleB[6]):
            cD_ifSat = True

    # Rules
    if addrCompare_tupleA[0] or addrCompare_tupleB[0]:
        if_encoding = False
        fwTarget_list = [False, False, False, False, False, False, False]
    elif cA_ifSat:
        if_encoding = True
        fwTarget_list = [False, False, False, addrCompare_tupleA[4], addrCompare_tupleA[3], False, False]
    elif cB_ifSat:
        if_encoding = True
        fwTarget_list = [False, False, False, False, False, addrCompare_tupleA[6], addrCompare_tupleA[5]]
    elif cC_ifSat:
        if_encoding = True
        fwTarget_list = [False, False, False, (addrCompare_tupleA[4] or addrCompare_tupleB[4]), (addrCompare_tupleA[3] or addrCompare_tupleB[3]), False, False]
        if (not addrCompare_tupleA[3]) and (not addrCompare_tupleA[4]):
            if (not addrCompare_tupleA[5]) and (not addrCompare_tupleA[6]):
                fwTarget_list[1] = addrCompare_tupleA[2]
                fwTarget_list[2] = addrCompare_tupleA[1]
            else:
                fwTarget_list[5] = addrCompare_tupleA[6]
                fwTarget_list[6] = addrCompare_tupleA[5]
        if (not addrCompare_tupleB[3]) and (not addrCompare_tupleB[4]):
            if (not addrCompare_tupleB[5]) and (not addrCompare_tupleB[6]):
                fwTarget_list[1] = addrCompare_tupleB[2]
                fwTarget_list[2] = addrCompare_tupleB[1]
            else:
                fwTarget_list[5] = addrCompare_tupleB[6]
                fwTarget_list[6] = addrCompare_tupleB[5]
    elif cD_ifSat:
        if_encoding = True
        fwTarget_list = [False, False, False, False, False, (addrCompare_tupleA[6] or addrCompare_tupleB[6]), (addrCompare_tupleA[5] or addrCompare_tupleB[5])]
        if (not addrCompare_tupleA[5]) and (not addrCompare_tupleA[6]):
            if (not addrCompare_tupleA[3]) and (not addrCompare_tupleA[4]):
                fwTarget_list[1] = addrCompare_tupleA[2]
                fwTarget_list[2] = addrCompare_tupleA[1]
            else:
                fwTarget_list[3] = addrCompare_tupleA[4]
                fwTarget_list[4] = addrCompare_tupleA[3]
        if (not addrCompare_tupleB[5]) and (not addrCompare_tupleB[6]):
            if (not addrCompare_tupleB[3]) and (not addrCompare_tupleB[4]):
                fwTarget_list[1] = addrCompare_tupleB[2]
                fwTarget_list[2] = addrCompare_tupleB[1]
            else:
                fwTarget_list[3] = addrCompare_tupleB[4]
                fwTarget_list[4] = addrCompare_tupleB[3]
    else:
        if_encoding = False
        fwTarget_list = [False, False, False, False, False, False, False]

    return if_encoding, tuple(fwTarget_list)
########################################################################################################################
########################################################################################################################


def arbiterNCModule_NCEncodingRules_NS(addrCompare_tuple01, addrCompare_tuple02):
    '''
    The strategy for encoding the packets from N and S ports.\n
    if_encoding - bool - If these two packets should be encoded.\n
    fwTarget_tuple - tuple(bool, bool, bool, bool, bool, bool, bool) - The packets should be forwarded to ports (IP, W, E, S, N, D, U).

    :param addrCompare_tuple01: tuple(bool, bool, bool, bool, bool, bool, bool) - See the return param of function arbiterModule_addrCompare.
    :param addrCompare_tuple02: tuple(bool, bool, bool, bool, bool, bool, bool) - See the return param of function arbiterModule_addrCompare.
    :return: if_encoding, fwTarget_tuple
    '''
    addrCompare_tupleA = copy.deepcopy(addrCompare_tuple01)
    addrCompare_tupleB = copy.deepcopy(addrCompare_tuple02)
    assert isinstance(addrCompare_tupleA, tuple) and len(addrCompare_tupleA) == 7
    assert isinstance(addrCompare_tupleB, tuple) and len(addrCompare_tupleB) == 7

    # Condition A: Two destinations locate at the same YZ plane as the local router
    cA_ifSat_c1 = False  # redundant. cA_ifSat_C1 is expected to be True.
    cA_ifSat = False
    if (not addrCompare_tupleA[3]) and (not addrCompare_tupleB[4]):  #
        cA_ifSat_c1 = True  #
    if (not addrCompare_tupleA[4]) and (not addrCompare_tupleB[3]):  #
        cA_ifSat_c1 = True  #
    # assert cA_ifSat_c1  #
    if addrCompare_tupleA[5] and addrCompare_tupleB[5]:
        cA_ifSat = True
    if addrCompare_tupleA[6] and addrCompare_tupleB[6]:
        cA_ifSat = True

    # Rules
    if addrCompare_tupleA[0] or addrCompare_tupleB[0]:
        if_encoding = False
        fwTarget_list = [False, False, False, False, False, False, False]
    elif cA_ifSat:
        if_encoding = True
        fwTarget_list = [False, False, False, False, False, addrCompare_tupleA[6], addrCompare_tupleA[5]]
    else:
        if_encoding = False
        fwTarget_list = [False, False, False, False, False, False, False]

    return if_encoding, tuple(fwTarget_list)