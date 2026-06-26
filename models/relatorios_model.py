from config.db import conectar

class RelatoriosModel():
    def listar_relatórios(self):
        conn = conectar()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""SELECT
                            m.nome as medico,
                            c.tipo_atendimento as tipo,
                            pl.nome as plano,
                            DATE_FORMAT(c.data, '%d/%m/%Y') as data
                        FROM Consulta c
                        JOIN Medico m ON c.id_medico = m.id_medico
                        JOIN Paciente p ON c.id_paciente = p.id_paciente
                        LEFT JOIN Plano pl ON p.id_plano = pl.id_plano
                        WHERE c.status_consulta = 'Atendido'
                       """)

        dados_relatorio = cursor.fetchall()
        cursor.close()
        conn.close()
        return dados_relatorio