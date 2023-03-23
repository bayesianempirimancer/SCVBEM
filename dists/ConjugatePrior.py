
class ConjugatePrior():
    def __init__(self):
        self.event_dim_0 = None # smallest possible event dimension
        self.event_dim = None
        self.event_shape = None
        self.batch_dim = None
        self.batch_shape = None
        self.nat_dim = None
        self.nat_parms_0 = None
        self.nat_parms = None

    def to_event(self,n):
        if n < 1:
            return self
        self.event_dim = self.event_dim + n
        self.batch_dim = self.batch_dim - n
        self.event_shape = self.batch_shape[-n:] + self.event_shape
        self.batch_shape = self.batch_shape[:-n]        
        return self

    def T(self,X):  # evaluate the sufficient statistic
        pass

    def ET(self):  # expected value of the sufficient statistic given the natural parameters
        pass

    def logZ(self):  # log partition function of the naturla parameters
        pass

    def logZ_ub(self): # upper bound on hte log partition function 
        pass

    def ss_update(self,ET,lr=1.0):
        self.nat_parms = ET + self.nat_parms_0

    def raw_update(self,X,p=None,lr=1.0):
        if p is None: 
            EmpT = self.T(X)
        else:
            sample_shape = p.shape[:-self.batch_dim]
            EmpT = self.T(X.view(sample_shape+self.batch_shape+self.event_shape))*p.view(p.shape + self.nat_dim*(1,)) 
        while EmpT.ndim > self.event_dim + self.batch_dim:
            EmpT = EmpT.sum(0)
        self.ss_update(EmpT,lr)

    def KL_qprior_event(self):  # returns the KL divergence between prior (nat_parms_0) and posterior (nat_parms)
        pass

    def KL_qprior(self):
        KL = KL_qprior_event(self)
        for i in range(self.event_dim - self.event_dim_0):
            KL = KL.sum(-1)

    def Elog_like_0(self,X):    # reuturns the likelihood of X under the default event_shape
        pass

    def Elog_like(self,X):   
        ELL = self.Elog_like_0(self,X)
        for i in range(self.event_dim - self.event_dim_0):
            ELL = ELL.sum(-1)
        return ELL

    def sample(self,sample_shape=()):
        pass

