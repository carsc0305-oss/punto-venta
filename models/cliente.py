class Cliente:

    def __init__(self, id=None, ruc="", razon_social="", estado="ACTIVO"):
        self.id = id
        self.ruc = ruc
        self.razon_social = razon_social
        self.estado = estado

    def __repr__(self):
        return (
            f"Cliente("
            f"id={self.id}, "
            f"ruc='{self.ruc}', "
            f"razon_social='{self.razon_social}', "
            f"estado='{self.estado}'"
            f")"
        )