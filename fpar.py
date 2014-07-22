class fpar(object):
  """ fitting parameter class """
  def __init__(self, f, repr):
    self.f    = f
    self.repr = repr

  def __call__(self, t):
    return self.f(self.repr, t)
