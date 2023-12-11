class Nivel:
    def __init__(self, items, plataformas, enemigos):
        self.items = items
        self.plataformas = plataformas
        self.enemigos = enemigos

    def update(self, delta_ms):
        # Lógica de actualización del nivel
        for item in self.items:
            item.update(delta_ms)

        for plataforma in self.plataformas:
            plataforma.update(delta_ms)

        for enemigo in self.enemigos:
            enemigo.update(delta_ms)

    def draw(self, screen):
        # Lógica de dibujo del nivel
        for item in self.items:
            item.draw(screen)

        for plataforma in self.plataformas:
            plataforma.draw(screen)

        for enemigo in self.enemigos:
            enemigo.draw(screen)