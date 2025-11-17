import pytest
from sqlalchemy.exc import IntegrityError
from database.models.voice_config import VoiceConfig

class TestVoiceConfigModel:
    """Pruebas del modelo VoiceConfig"""

    def test_crear_configuracion_voz_por_defecto(self, session):
        voice_config = VoiceConfig()
        session.add(voice_config)
        session.commit()

        assert voice_config.id == 1
        assert voice_config.voice_gender == "FEMALE"
        assert voice_config.voice_pitch == 1.0

    def test_configuracion_voz_personalizada(self, session):
        voice_config = VoiceConfig(
            voice_gender="MALE",
            voice_pitch=1.5
        )
        session.add(voice_config)
        session.commit()

        assert voice_config.id == 1
        assert voice_config.voice_gender == "MALE"
        assert voice_config.voice_pitch == 1.5

    def test_set_voice_gender_valido(self):
        voice_config = VoiceConfig()
        
        voice_config.set_voice_gender("FEMALE")
        assert voice_config.voice_gender == "FEMALE"
        
        voice_config.set_voice_gender("MALE")
        assert voice_config.voice_gender == "MALE"
        
        voice_config.set_voice_gender("ROBOTIC")
        assert voice_config.voice_gender == "ROBOTIC"

    def test_set_voice_gender_invalido(self):
        voice_config = VoiceConfig()
        
        with pytest.raises(ValueError) as exc_info:
            voice_config.set_voice_gender("INVALID")
        
        assert "voice_gender inválido" in str(exc_info.value)
        assert "FEMALE" in str(exc_info.value)
        assert "MALE" in str(exc_info.value)
        assert "ROBOTIC" in str(exc_info.value)

    def test_to_dict(self):
        voice_config = VoiceConfig(
            voice_gender="MALE",
            voice_pitch=1.2
        )
        
        result = voice_config.to_dict()
        
        expected = {
            "voice_gender": "MALE",
            "voice_pitch": 1.2
        }
        assert result == expected

    def test_actualizar_configuracion_existente(self, session):
        # Crear configuración inicial
        voice_config = VoiceConfig()
        session.add(voice_config)
        session.commit()

        # Actualizar la configuración
        voice_config_db = session.get(VoiceConfig, 1)
        voice_config_db.set_voice_gender("ROBOTIC")
        voice_config_db.voice_pitch = 0.8
        session.commit()

        # Verificar cambios
        voice_config_actualizada = session.get(VoiceConfig, 1)
        assert voice_config_actualizada.voice_gender == "ROBOTIC"
        assert voice_config_actualizada.voice_pitch == 0.8

    def test_configuracion_unica(self, session):
        # Solo debe existir una configuración de voz
        voice_config1 = VoiceConfig()
        session.add(voice_config1)
        session.commit()

        # Intentar crear segunda configuración debería fallar
        # Primero necesitamos hacer rollback de la sesión actual
        session.expunge_all()
        
        voice_config2 = VoiceConfig(id=1)  # Mismo ID
        session.add(voice_config2)
        
        # Esto debería fallar porque el ID ya existe
        with pytest.raises(IntegrityError):
            session.commit()
        session.rollback()

    def test_actualizar_configuracion_existente_sin_duplicar(self, session):
        # En lugar de crear nueva, actualizar la existente
        voice_config = VoiceConfig()
        session.add(voice_config)
        session.commit()

        # Actualizar la configuración existente
        voice_config.voice_gender = "MALE"
        voice_config.voice_pitch = 1.3
        session.commit()

        # Verificar que solo hay una configuración
        count = session.query(VoiceConfig).count()
        assert count == 1
        
        config = session.get(VoiceConfig, 1)
        assert config.voice_gender == "MALE"
        assert config.voice_pitch == 1.3

    def test_valores_limite_pitch(self, session):
        voice_config = VoiceConfig(voice_pitch=0.5)
        session.add(voice_config)
        session.commit()

        voice_config_db = session.get(VoiceConfig, 1)
        assert voice_config_db.voice_pitch == 0.5

        # Actualizar a otro valor
        voice_config_db.voice_pitch = 2.0
        session.commit()
        assert voice_config_db.voice_pitch == 2.0

    def test_reinicializar_configuracion(self, session):
        # Crear configuración personalizada
        voice_config = VoiceConfig(voice_gender="MALE", voice_pitch=1.5)
        session.add(voice_config)
        session.commit()

        # Reinicializar a valores por defecto
        voice_config_db = session.get(VoiceConfig, 1)
        voice_config_db.voice_gender = "FEMALE"
        voice_config_db.voice_pitch = 1.0
        session.commit()

        voice_config_final = session.get(VoiceConfig, 1)
        assert voice_config_final.voice_gender == "FEMALE"
        assert voice_config_final.voice_pitch == 1.0