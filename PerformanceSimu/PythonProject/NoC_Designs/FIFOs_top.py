# FIFOs
import copy

import Simulation.SimuConfigurationClass as imported_ActiveConfiguration
import Arbiter_Logic.FixedPriority as imported_FixedPriorityArbiter
import Arbiter_Logic.FixedPriority_NC as imported_NCFixedPriorityArbiter

class FIFOsTop:
    def __init__(self, flit_depth, flit_bw, fifo_id=None):
        assert isinstance(flit_depth, int) and (flit_depth > 0)
        assert isinstance(flit_bw, int) and (flit_bw > 0)
        self._param_FIFOID = copy.deepcopy(fifo_id)
        self._param_fifoDepth = copy.deepcopy(flit_depth)
        self._param_fifoBitWidth = copy.deepcopy(flit_bw)
        self._initializeMemory()

    def _initializeMemory(self):
        self._memory_tuple = ()
        self._memoryState_flitCount = 0

    def getParam_fifoDepth(self):
        '''
        Return the depth of FIFO (the maximum number of flits that can be stored in memory).
        :return:
        '''
        return copy.deepcopy(self._param_fifoDepth)

    def getParam_fifoBitWidth(self):
        '''
        The bit-width of each flit.
        :return:
        '''
        return copy.deepcopy(self._param_fifoBitWidth)

    def memOp_getAllFlits(self):
        assert isinstance(self._memory_tuple, tuple)
        return copy.deepcopy(self._memory_tuple)

    def getState_flitCount(self):
        '''
        Return the number of flits in memory.
        :return:
        '''
        assert len(self.memOp_getAllFlits()) == self._memoryState_flitCount
        return copy.deepcopy(self._memoryState_flitCount)

    def getState_ifFull(self):
        '''
        If the FIFO is full
        :return: bool
        '''
        if self.getState_flitCount() < self.getParam_fifoDepth():
            return False
        elif self.getState_flitCount() == self.getParam_fifoDepth():
            return True
        else:
            assert False

    def getState_ifEmpty(self):
        '''
        If the FIFO is empty.
        :return: bool
        '''
        if self.getState_flitCount() == 0:
            return True
        else:
            assert self.getState_flitCount() <= self.getParam_fifoDepth()

    def memOp_getFirstFlit(self):
        if self.getState_ifEmpty():
            return None
        else:
            firstFlit = self.memOp_getAllFlits()[0]
            assert isinstance(firstFlit, tuple) and (len(firstFlit) == self.getParam_fifoBitWidth())
            return copy.deepcopy(firstFlit)

    def memOp_deleteFirstFlit(self):
        '''
        Delete the first flit
        :return:
        '''
        assert not self.getState_ifEmpty()
        old_memList = list(self.memOp_getAllFlits())
        new_memList = old_memList.pop(0)
        new_memTuple = tuple(new_memList)
        new_memFlitCnt = len(new_memTuple)
        assert new_memFlitCnt == (self.getState_flitCount() - 1)

        self._memory_tuple = copy.deepcopy(new_memTuple)
        self._memoryState_flitCount = copy.deepcopy(new_memFlitCnt)

    def memOp_writeOneFlit(self, flitNew):
        assert not self.getState_ifFull()
        assert isinstance(flitNew, tuple) and (len(flitNew) == self.getParam_fifoBitWidth())
        current_memList = list(self.memOp_getAllFlits())
        current_memList.append(copy.deepcopy(flitNew))
        new_memTuple = tuple(current_memList)
        new_memFlitCnt = len(new_memTuple)
        assert new_memFlitCnt == (self.getState_flitCount() + 1)

        self._memory_tuple = copy.deepcopy(new_memTuple)
        self._memoryState_flitCount = copy.deepcopy(new_memFlitCnt)

