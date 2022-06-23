import numpy
from drawSvg import Path


class BasicPlot(Path):
    """Takes standard keyword arguments from drawSvg.Path, but takes a list of coords (tuple or list for coord pairs)
    as the required first positional argument"""
    TAG_NAME = 'path'
    
    def __init__(self, coords: list[tuple],d='', **kwargs) -> None:
        super().__init__(d=d, **kwargs)
        self.coords = coords
        fc = self.coords.pop(0)
        self.M(fc[0],fc[1])
        for xp, yp in self.coords:
            self.L(xp, yp)


class CatmullRomChainPath(Path):
    """Takes standard keyword arguments from drawSvg.Path, but takes a list of coords (tuple or list for coord pairs)
    as the required first positional argument.
    Additional Keyword args:
    resolution: (default 25) how many points are calculated between each point given
    alpha: Parametric constant according to the Catmull algorithm. (default .5)
        0.5 -> centripetal spline
        0.0 -> uniform spline
        1.0 -> chordal spline"""

    TAG_NAME = 'path'
    def __init__(self, coords: list[tuple], d='', resolution=25, alpha=0.5, **kwargs) -> None:
        super().__init__(d=d,**kwargs)
        self.coords = coords
        P = coords
        sz = len(self.coords)
        C = []
        for i in range(sz-3):
            c = CatmullRomChainPath.catmull_rom_spline(P[i], P[i+1], P[i+2], P[i+3],nPoints=resolution,_alpha=alpha)
            C.extend(c)
        x,y = zip(*C)
        self.x = list(x)
        self.y = list(y)
        self.M(self.x.pop(0),self.y.pop(0))
        for xval,yval in zip(self.x,self.y):
            self.L(xval, yval)
    
    def coord_list(self):
        return [(xval, yval) for xval,yval in zip(self.x,self.y)]



        

    @staticmethod
    def catmull_rom_spline(P0, P1, P2, P3, nPoints=25,_alpha=0.5):
        """
        P0, P1, P2, and P3 should be (x,y) point pairs that define the Catmull-Rom spline.
        nPoints is the number of points to include in this curve segment.
        """
        # Convert the points to numpy so that we can do array multiplication
        P0, P1, P2, P3 = map(numpy.array, [P0, P1, P2, P3])

        # Premultiplied power constant for the following tj() function.
        alpha = _alpha/2
        def tj(ti, Pi, Pj):
            xi, yi = Pi
            xj, yj = Pj
            return ((xj-xi)**2 + (yj-yi)**2)**alpha + ti

        # Calculate t0 to t4
        t0 = 0
        t1 = tj(t0, P0, P1)
        t2 = tj(t1, P1, P2)
        t3 = tj(t2, P2, P3)

        # Only calculate points between P1 and P2
        t = numpy.linspace(t1, t2, nPoints)

        # Reshape so that we can multiply by the points P0 to P3
        # and get a point for each value of t.
        t = t.reshape(len(t), 1)
        A1 = (t1-t)/(t1-t0)*P0 + (t-t0)/(t1-t0)*P1
        A2 = (t2-t)/(t2-t1)*P1 + (t-t1)/(t2-t1)*P2
        A3 = (t3-t)/(t3-t2)*P2 + (t-t2)/(t3-t2)*P3
        B1 = (t2-t)/(t2-t0)*A1 + (t-t0)/(t2-t0)*A2
        B2 = (t3-t)/(t3-t1)*A2 + (t-t1)/(t3-t1)*A3

        C = (t2-t)/(t2-t1)*B1 + (t-t1)/(t2-t1)*B2
        return C
    
    
