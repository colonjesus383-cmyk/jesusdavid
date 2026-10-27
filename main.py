
import pytest

from personajes import Personaje, Guerrero, Mago, Arquero, Combate


def test_creacion_personajes():
    assert Guerrero("Arthas", 100, 30, 20).vida == 100
    assert Mago("Gandalf", 80, 40, 10).ataque == 40
    assert Arquero("Legolas", 90, 35, 15).defensa == 15


@pytest.mark.parametrize("vida", [-1, 101])
def test_vida_invalida(vida):
    with pytest.raises(ValueError):
        Guerrero("Arthas", vida, 30, 20)


def test_nombre_vacio():
    with pytest.raises(ValueError):
        Guerrero("", 100, 30, 20)


def test_ataques_especiales():
    guerrero = Guerrero("Arthas", 100, 30, 20)
    mago_objetivo = Mago("Gandalf", 80, 40, 10)
    assert guerrero.atacar(mago_objetivo) == 26

    mago = Mago("Merlin", 80, 40, 10)
    objetivo = Guerrero("Thor", 100, 20, 20)
    assert mago.atacar(objetivo) == 40

    arquero = Arquero("Legolas", 90, 35, 15)
    objetivo2 = Guerrero("Boromir", 100, 20, 20)
    assert arquero.atacar(objetivo2) == 30


def test_vida_no_negativa():
    mago = Mago("Merlin", 80, 200, 10)
    objetivo = Guerrero("Arthas", 10, 20, 20)
    assert mago.atacar(objetivo) == 10
    assert objetivo.vida == 0


def test_personaje_derrotado_no_ataca():
    guerrero = Guerrero("Arthas", 0, 30, 20)
    objetivo = Mago("Gandalf", 80, 40, 10)

    with pytest.raises(ValueError):
        guerrero.atacar(objetivo)


def test_personaje_abstracto():
    with pytest.raises(TypeError):
        Personaje("Base", 100, 10, 5)


def test_combate_con_ganador():
    guerrero = Guerrero("Arthas", 100, 30, 20)
    mago = Mago("Gandalf", 80, 40, 10)
    combate = Combate(guerrero, mago)

    ganador = combate.iniciar()

    assert ganador is mago
    assert combate.terminado


def test_empate_tecnico():
    arquero1 = Arquero("Legolas", 100, 10, 20)
    arquero2 = Arquero("Guardia", 100, 10, 20)
    combate = Combate(arquero1, arquero2)

    ganador = combate.iniciar()

    assert ganador is None
    assert combate.empate
    assert combate.terminado


def ejecutar_programa():
    arthas = Guerrero("Arthas", 100, 30, 20)
    gandalf = Mago("Gandalf", 80, 40, 10)
    Combate(arthas, gandalf).iniciar()


if __name__ == "__main__":
    ejecutar_programa()
