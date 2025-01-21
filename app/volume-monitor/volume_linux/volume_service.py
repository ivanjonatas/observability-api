import psutil

class VolumeService:
    @staticmethod
    def listar_volumes():
        volumes = []
        for part in psutil.disk_partitions():
            if "rw" in part.opts:  # Considera apenas volumes graváveis
                uso = psutil.disk_usage(part.mountpoint)
                volumes.append({
                    "ponto_de_montagem": part.mountpoint,
                    "total": uso.total,
                    "usado": uso.used,
                    "livre": uso.free,
                    "percentual": uso.percent
                })
        return volumes
