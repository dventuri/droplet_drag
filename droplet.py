import math
import warnings


from constants import MU_FLUID


class Droplet:

    def __init__(self, Rep: float = 1, mu_droplet: float = 0.0010005):
        self.__Rep = Rep
        self.__mu = mu_droplet
        self.__gamma = self.calc_gamma(mu_droplet)
        self.check_negative_Rep()
        self.check_negative_gamma()

    def calc_gamma(self, mu_droplet) -> float:
        return mu_droplet/MU_FLUID

    def check_negative_Rep(self) -> None:
        if (self.__Rep < 0):
            raise ValueError("Negative 'Rep' value not allowed")

    def check_negative_gamma(self) -> None:
        if (self.__gamma < 0):
            raise ValueError("Negative viscosity value not allowed")

    def schiller_and_naumann_1935(self) -> float:

        if (self.__Rep < 0.1):
            Cd = 24/self.__Rep
        elif (self.__Rep < 1000):
            Cd = 24/self.__Rep * (1 + 0.15*(self.__Rep**0.687))
        else:
            Cd = 0.44

        return Cd

    def putnam_1961(self) -> float:

        if (self.__Rep < 1000):
            Cd = 24/self.__Rep * (1 + 1/6*(self.__Rep**(2/3)))
        else:
            Cd = 0.44
            warnings.warn(
                "'Rep' value above correlation limit, using '0.44' as estimate"
                )

        return Cd

    def hadamard_and_rybczynski_1911(self) -> float:
        # apud Feng and Michelides (2001)
        # Creeping flow

        if (self.__Rep > 0.1):
            warnings.warn(
                "Correlation suitable only for creeping flow"
                )

        Cd = 8/self.__Rep*((3*self.__gamma + 2)/(self.__gamma + 1))

        return Cd

    def feng_and_michaelides_2001(self) -> float:

        if (self.__Rep <= 5):
            Cd = self.hadamard_and_rybczynski_1911() * (
                1 + 0.05*((3*self.__gamma + 2)/(self.__gamma + 1)*self.__Rep)
            ) - (
                0.01*(3*self.__gamma + 2)/(self.__gamma + 1)*(
                    self.__Rep*math.log(self.__Rep)
                )
            )
        elif (self.__Rep < 1000):

            Cd_2 = 17*(self.__Rep**(-2/3))

            if (self.__gamma < 2):
                Cd_0 = 48/self.__Rep*(
                    1 + 2.21/math.sqrt(self.__Rep) - 2.14/math.sqrt(self.__Rep)
                )

                Cd = (
                    (2 - self.__gamma)/2*Cd_0
                ) + (
                    4*self.__gamma/(6 + self.__gamma)*Cd_2
                )
            else:
                Cd_inf = self.putnam_1961()

                Cd = (
                    4/(self.__gamma + 2)*Cd_2
                ) + (
                    (self.__gamma - 2)/(self.__gamma + 2)*Cd_inf
                )

        return Cd

    @property
    def Rep(self):
        return self.__Rep

    @property
    def mu(self):
        return self.__mu

    @property
    def gamma(self):
        return self.__gamma

    @Rep.setter
    def Rep(self, Rep):
        self.__Rep = Rep

    @mu.setter
    def mu(self, mu_droplet):
        self.__mu = mu_droplet
        self.__gamma = self.calc_gamma(mu_droplet)
