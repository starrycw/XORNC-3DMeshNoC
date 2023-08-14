import copy


class SimuConfigs:
    '''
    Contains the value of the configurable params for simulation.
    '''

    def __init__(self, param_flitBitWidth = 64, param_addrBitWidth_tuple = (2, 2, 2), param_FIFOFlitDepth = 3):
        '''

        :param param_flitBitWidth: int - The bit-width of each flit. The default value is 64.
        :param param_addrBitWidth_tuple: tuple(int, int, int) - The bit-width of the (X, Y, X) address. The default value is (2, 2, 2)
        '''
        assert isinstance(param_addrBitWidth_tuple, tuple) and len(param_addrBitWidth_tuple) == 3
        assert isinstance(param_addrBitWidth_tuple, int) and ( param_flitBitWidth > 2 * (param_addrBitWidth_tuple[0] + param_addrBitWidth_tuple[1] + param_addrBitWidth_tuple[2]) )
        assert isinstance(param_FIFOFlitDepth, int) and (param_FIFOFlitDepth > 0)

        self._param_flitBitWidth = param_flitBitWidth
        self._param_addrBitWidth = copy.deepcopy(param_addrBitWidth_tuple)
        self._param_FIFO_flitDepth = copy.deepcopy(param_FIFOFlitDepth)


    def getParam_flitBitWidth(self):
        '''
        Return the bit-width of each flit.
        :return: int
        '''
        return self._param_flitBitWidth

    def getParam_flitAddrBitWidth_tuple(self):
        '''
        Return the bit-width of the (X, Y, X) address.
        :return: tuple(int, int, int)
        '''
        return copy.deepcopy(self._param_addrBitWidth)

    def getParam_flitAddrBitWidth_X(self):
        addrBW_tuple = self.getParam_flitAddrBitWidth_tuple()
        return addrBW_tuple[0]

    def getParam_flitAddrBitWidth_Y(self):
        addrBW_tuple = self.getParam_flitAddrBitWidth_tuple()
        return addrBW_tuple[1]

    def getParam_flitAddrBitWidth_Z(self):
        addrBW_tuple = self.getParam_flitAddrBitWidth_tuple()
        return addrBW_tuple[2]

    def getParam_FIFOFlitDepth(self):
        return copy.deepcopy(self._param_FIFO_flitDepth)

    # Flit:
    #   uncoded head flit (head): [0] = True, [1] = True, [2] = True, [3:x] is address
    #   encoded head flit (NChead): [0] = True, [1] = True, [2] = False, [3:x] is address
    #   payload flit (payload): [0] = False, [1:x] is payload data
    #   tail flit (tail): [0] = True, [1] = False
    def flitAnalyse_getType(self, flit_tuple):
        '''
        Return the type of a flit.
        :param flit_tuple: tuple(bool, bool, ...) - The input flit.
        :return: string - in ("head", "NChead", "payload", "tail")
        '''
        assert isinstance(flit_tuple, tuple) and ( len(flit_tuple) == self.getParam_flitBitWidth() )
        if (not flit_tuple[0]):
            type_str = "payload"
        elif (not flit_tuple[1]):
            type_str = "tail"
        elif flit_tuple[2]:
            type_str = "head"
        else:
            type_str = "NChead"
        return type_str

    def flitAnalyse_getAddrA(self, flit_tuple):
        '''
        Return the Address A in a head flit. Note that this function does not check the flit type!

        :param flit_tuple: tuple(bool, bool, ...) - The input flit.
        :return: tuple(int, int, int) - (AddrA-X, AddrA-Y, AddrA-Z)
        '''
        addrX_bLen = self.getParam_flitAddrBitWidth_X()
        addrY_bLen = self.getParam_flitAddrBitWidth_Y()
        addrZ_bLen = self.getParam_flitAddrBitWidth_Z()

        addrX_value = 0
        weight_value = 1
        for idx_i in range((2 + addrX_bLen),  2, -1):
            if flit_tuple[idx_i]:
                addrX_value = addrX_value + weight_value
            weight_value = weight_value * 2

        addrY_value = 0
        weight_value = 1
        for idx_i in range((2 + addrX_bLen + addrY_bLen), (2 + addrX_bLen), -1):
            if flit_tuple[idx_i]:
                addrY_value = addrY_value + weight_value
            weight_value = weight_value * 2

        addrZ_value = 0
        weight_value = 1
        for idx_i in range((2 + addrX_bLen + addrY_bLen + addrZ_bLen), (2 + addrX_bLen + addrY_bLen), -1):
            if flit_tuple[idx_i]:
                addrZ_value = addrZ_value + weight_value
            weight_value = weight_value * 2

        return (addrX_value, addrY_value, addrZ_value)

    def flitAnalyse_getAddrB(self, flit_tuple):
        '''
        Return the Address B in a head flit. Note that this function does not check the flit type!

        :param flit_tuple: tuple(bool, bool, ...) - The input flit.
        :return: tuple(int, int, int) - (AddrA-X, AddrA-Y, AddrA-Z)
        '''
        addrX_bLen = self.getParam_flitAddrBitWidth_X()
        addrY_bLen = self.getParam_flitAddrBitWidth_Y()
        addrZ_bLen = self.getParam_flitAddrBitWidth_Z()
        initialIdx = 2 + addrX_bLen + addrY_bLen + addrZ_bLen

        addrX_value = 0
        weight_value = 1
        for idx_i in range((initialIdx + addrX_bLen),  initialIdx, -1):
            if flit_tuple[idx_i]:
                addrX_value = addrX_value + weight_value
            weight_value = weight_value * 2

        addrY_value = 0
        weight_value = 1
        for idx_i in range((initialIdx + addrX_bLen + addrY_bLen), (initialIdx + addrX_bLen), -1):
            if flit_tuple[idx_i]:
                addrY_value = addrY_value + weight_value
            weight_value = weight_value * 2

        addrZ_value = 0
        weight_value = 1
        for idx_i in range((initialIdx + addrX_bLen + addrY_bLen + addrZ_bLen), (initialIdx + addrX_bLen + addrY_bLen), -1):
            if flit_tuple[idx_i]:
                addrZ_value = addrZ_value + weight_value
            weight_value = weight_value * 2

        return (addrX_value, addrY_value, addrZ_value)