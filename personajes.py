
from abc import ABC, abstractmethod
from math import floor


class Personaje(ABC):
    def __init__(self, nombre, vida, ataque, defensa):
        self.nombre = nombre
        self.vida = vida
        self.ataque = ataque
        self.defensa = defensa

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El nombre no puede estar vacío.")
        self.__nombre = valor.strip()

    @property
    def vida(self):
        return self.__vida

    @vida.setter
    def vida(self, valor):
        if isinstance(valor, bool) or not isinstance(valor, int):
            raise TypeError("La vida debe ser un entero.")
        if not 0 <= valor <= 100:
            raise ValueError("La vida debe estar entre 0 y 100.")
        self.__vida = valor

    @property
    def ataque(self):
        return self.__ataque

    @ataque.setter
    def ataque(self, valor):
        if isinstance(valor, bool) or not isinstance(valor, int):
            raise TypeError("El ataque debe ser un entero.")
        if valor <= 0:
            raise ValueError("El ataque debe ser positivo.")
        self.__ataque = valor

    @property
    def defensa(self):
        return self.__defensa

    @defensa.setter
    def defensa(self, valor):
        if isinstance(valor, bool) or not isinstance(valor, int):
            raise TypeError("La defensa debe ser un entero.")
        if valor < 0:
            raise ValueError("La defensa no puede ser negativa.")
        self.__defensa = valor

    def get_nombre(self):
        return self.nombre

    def set_nombre(self, valor):
        self.nombre = valor

    def get_vida(self):
        return self.vida

    def set_vida(self, valor):
        self.vida = valor

    def get_ataque(self):
        return self.ataque

    def set_ataque(self, valor):
        self.ataque = valor

    def get_defensa(self):
        return self.defensa

    def set_defensa(self, valor):
        self.defensa = valor

    def recibir_danio(self, cantidad):
        if isinstance(cantidad, bool) or not isinstance(
            cantidad, (int, float)
        ):
            raise TypeError("El daño debe ser numérico.")
        if cantidad < 0:
            raise ValueError("El daño no puede ser negativo.")

        danio = min(self.vida, floor(cantidad))
        self.vida = max(0, self.vida - danio)
        return danio

    def esta_vivo(self):
        return self.vida > 0

    def mostrar_estado(self):
        return (
            f"{self.nombre} | Vida: {self.vida} | "
            f"Ataque: {self.ataque} | Defensa: {self.defensa}"
        )

    def _validar_objetivo(self, objetivo):
        if not isinstance(objetivo, Personaje):
            raise TypeError("El objetivo debe ser un personaje.")
        if objetivo is self:
            raise ValueError("No puedes atacarte a ti mismo.")
        if not self.esta_vivo():
            raise ValueError("Un personaje derrotado no puede atacar.")
        if not objetivo.esta_vivo():
            raise ValueError("El objetivo ya está derrotado.")

    @abstractmethod
    def atacar(self, objetivo):
        pass


class Guerrero(Personaje):
    def atacar(self, objetivo):
        self._validar_objetivo(objetivo)
        danio = max(0, floor(self.ataque * 1.20 - objetivo.defensa))
        return objetivo.recibir_danio(danio)


class Mago(Personaje):
    def atacar(self, objetivo):
        self._validar_objetivo(objetivo)
        return objetivo.recibir_danio(self.ataque)


class Arquero(Personaje):
    def atacar(self, objetivo):
        self._validar_objetivo(objetivo)

        if self.ataque > objetivo.defensa:
            danio = (self.ataque - objetivo.defensa) * 2
        else:
            danio = 0

        return objetivo.recibir_danio(danio)


class Combate:
    def __init__(self, personaje1, personaje2):
        if not isinstance(personaje1, Personaje):
            raise TypeError("El primer participante no es válido.")
        if not isinstance(personaje2, Personaje):
            raise TypeError("El segundo participante no es válido.")
        if personaje1 is personaje2:
            raise ValueError("Se necesitan dos personajes diferentes.")

        self.personaje1 = personaje1
        self.personaje2 = personaje2
        self.turno_actual = personaje1
        self.ganador = None
        self.terminado = False
        self.empate = False
        self.rondas = 0

    def cambiar_turno(self):
        if self.turno_actual is self.personaje1:
            self.turno_actual = self.personaje2
        else:
            self.turno_actual = self.personaje1

    def verificar_ganador(self):
        if not self.personaje1.esta_vivo():
            self.ganador = (
                self.personaje2 if self.personaje2.esta_vivo() else None
            )
            self.terminado = True
        elif not self.personaje2.esta_vivo():
            self.ganador = self.personaje1
            self.terminado = True

        return self.ganador

    def mostrar_resultado(self):
        print("\n=== RESULTADO DEL COMBATE ===")
        if self.ganador:
            print(f"Ganador: {self.ganador.nombre}")
        elif self.empate:
            print("El combate terminó en empate.")
        else:
            print("El combate todavía no ha terminado.")

        print(self.personaje1.mostrar_estado())
        print(self.personaje2.mostrar_estado())

    def iniciar(self):
        if self.terminado:
            self.mostrar_resultado()
            return self.ganador

        if not self.personaje1.esta_vivo() or not self.personaje2.esta_vivo():
            self.verificar_ganador()
            self.mostrar_resultado()
            return self.ganador

        print("\n=== GUARDIANS OF THE ANCIENT KINGDOM ===")
        print(self.personaje1.mostrar_estado())
        print(self.personaje2.mostrar_estado())

        while self.rondas < 50:
            self.rondas += 1
            danio_ronda = 0
            print(f"\n--- Ronda {self.rondas} ---")

            for _ in range(2):
                atacante = self.turno_actual
                objetivo = (
                    self.personaje2
                    if atacante is self.personaje1
                    else self.personaje1
                )

                if atacante.esta_vivo() and objetivo.esta_vivo():
                    danio = atacante.atacar(objetivo)
                    danio_ronda += danio
                    print(
                        f"{atacante.nombre} ataca a {objetivo.nombre}. "
                        f"Daño efectivo: {danio}"
                    )
                    print(self.personaje1.mostrar_estado())
                    print(self.personaje2.mostrar_estado())

                self.verificar_ganador()
                if self.terminado:
                    self.mostrar_resultado()
                    return self.ganador

                self.cambiar_turno()

            if danio_ronda == 0:
                self.empate = True
                self.terminado = True
                self.mostrar_resultado()
                return None

        self.empate = True
        self.terminado = True
        print("\nSe alcanzó el límite de 50 rondas.")
        self.mostrar_resultado()
        return None
