from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, DateTime, and_
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    nombre: Mapped[str] = mapped_column(String(50), nullable=True)
    apellido: Mapped[str] = mapped_column(String(50), nullable=True)
    fecha_suscripcion: Mapped[datetime] = mapped_column(DateTime(), default=datetime.utcnow)

    favoritos: Mapped[list["Favorito"]] = relationship(
        "Favorito",
        back_populates="usuario",
        cascade="all, delete"
    )

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "fecha_suscripcion": self.fecha_suscripcion.isoformat()
        }

class Personaje(db.Model):
    __tablename__ = "personaje"
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    genero: Mapped[str] = mapped_column(String(50))
    altura: Mapped[str] = mapped_column(String(50))
    color_pelo: Mapped[str] = mapped_column(String(50))
    color_piel: Mapped[str] = mapped_column(String(50))
    color_ojos: Mapped[str] = mapped_column(String(50))

    favoritos: Mapped[list["Favorito"]] = relationship(
        "Favorito",
        primaryjoin=lambda: and_(
            Favorito.objeto_id == Personaje.id,
            Favorito.tipo == "personaje"
        ),
        viewonly=True
    )

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "genero": self.genero,
            "altura": self.altura,
            "color_pelo": self.color_pelo,
            "color_piel": self.color_piel,
            "color_ojos": self.color_ojos
        }

class Planeta(db.Model):
    __tablename__ = "planeta"
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    clima: Mapped[str] = mapped_column(String(100))
    terreno: Mapped[str] = mapped_column(String(100))
    poblacion: Mapped[str] = mapped_column(String(100))

    favoritos: Mapped[list["Favorito"]] = relationship(
        "Favorito",
        primaryjoin=lambda: and_(
            Favorito.objeto_id == Planeta.id,
            Favorito.tipo == "planeta"
        ),
        viewonly=True
    )

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "clima": self.clima,
            "terreno": self.terreno,
            "poblacion": self.poblacion
        }

class Vehiculo(db.Model):
    __tablename__ = "vehiculo"
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    modelo: Mapped[str] = mapped_column(String(100))
    fabricante: Mapped[str] = mapped_column(String(100))
    costo: Mapped[str] = mapped_column(String(50))
    longitud: Mapped[str] = mapped_column(String(50))

    favoritos: Mapped[list["Favorito"]] = relationship(
        "Favorito",
        primaryjoin=lambda: and_(
            Favorito.objeto_id == Vehiculo.id,
            Favorito.tipo == "vehiculo"
        ),
        viewonly=True
    )

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "modelo": self.modelo,
            "fabricante": self.fabricante,
            "costo": self.costo,
            "longitud": self.longitud
        }

class Favorito(db.Model):
    __tablename__ = "favorito"
    id: Mapped[int] = mapped_column(primary_key=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    tipo: Mapped[str] = mapped_column(String(50), nullable=False)  # 'personaje', 'planeta' o 'vehiculo'
    objeto_id: Mapped[int] = mapped_column(nullable=False)

    usuario: Mapped["User"] = relationship("User", back_populates="favoritos")

    personaje: Mapped["Personaje"] = relationship(
        "Personaje",
        primaryjoin=lambda: and_(
            Favorito.objeto_id == Personaje.id,
            Favorito.tipo == "personaje"
        ),
        viewonly=True
    )
    planeta: Mapped["Planeta"] = relationship(
        "Planeta",
        primaryjoin=lambda: and_(
            Favorito.objeto_id == Planeta.id,
            Favorito.tipo == "planeta"
        ),
        viewonly=True
    )
    vehiculo: Mapped["Vehiculo"] = relationship(
        "Vehiculo",
        primaryjoin=lambda: and_(
            Favorito.objeto_id == Vehiculo.id,
            Favorito.tipo == "vehiculo"
        ),
        viewonly=True
    )

    def serialize(self):
        data = {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "tipo": self.tipo,
            "objeto_id": self.objeto_id
        }
        # incluimos detalle según el tipo
        if self.personaje:
            data["detalle"] = self.personaje.serialize()
        elif self.planeta:
            data["detalle"] = self.planeta.serialize()
        elif self.vehiculo:
            data["detalle"] = self.vehiculo.serialize()
        return data
