"""
Utilidades compartidas por las visualizaciones interactivas de las
preguntas del examen: un panel de leyenda numerada donde, al pasar el
mouse sobre una fila, esa fila Y la parte del grafico principal que le
corresponde se ponen a PARPADEAR (para saber a que parte del grafico
pertenece cada termino).

Se separo aqui porque la pregunta 15 y la pregunta 16 usan exactamente
el mismo mecanismo de leyenda + parpadeo; asi evitamos tener el mismo
codigo de eventos de mouse y timers duplicado en cada archivo.
"""

from matplotlib.patches import Rectangle


class LeyendaInteractiva:
    """Construye el panel de leyenda numerada y conecta el parpadeo.

    Uso tipico:
        leyenda = LeyendaInteractiva(fig, ax_leyenda, ITEMS, 'Titulo')
        leyenda.registrar_badge(1, mi_texto_numerado_en_el_3d)
        leyenda.registrar_halo(1, [mi_linea_halo, mi_scatter_halo])
        leyenda.iniciar_parpadeo()
    """

    def __init__(self, fig, ax_leyenda, items, titulo='Terminos'):
        self.fig = fig
        self.ax_leyenda = ax_leyenda
        self.items = items  # lista de (numero, color, titulo_fila, subtitulo)
        self.numeros = [it[0] for it in items]

        self.leyenda_y = {}
        self.rects = {}
        self.scatters = {}
        self.badges = {}   # numero -> artista de texto numerado sobre el grafico
        self.halos = {}    # numero -> lista de artistas que deben parpadear

        self.hover_num = None
        self._blink_on = False
        self._ultimo_num = None
        self.timer = None

        self._construir(titulo)
        self.fig.canvas.mpl_connect('motion_notify_event', self._on_motion)

    # -----------------------------------------------------------------
    def _construir(self, titulo):
        ax = self.ax_leyenda
        ax.axis('off')
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)

        self.fila_alto = 1.0 / (len(self.items) + 0.5)
        for i, (num, color, titulo_fila, sub) in enumerate(self.items):
            y_centro = 1 - (i + 0.8) * self.fila_alto
            self.leyenda_y[num] = y_centro

            rect = Rectangle((0.0, y_centro - self.fila_alto * 0.42), 1.0,
                              self.fila_alto * 0.84, transform=ax.transData,
                              facecolor=color, alpha=0.0, zorder=0, linewidth=0)
            ax.add_patch(rect)
            self.rects[num] = rect

            scat = ax.scatter([0.06], [y_centro], s=420, color=color, zorder=2,
                               edgecolors='black', linewidths=0.5)
            self.scatters[num] = scat
            ax.text(0.06, y_centro, str(num), color='white', fontsize=10,
                     fontweight='bold', ha='center', va='center', zorder=3)
            ax.text(0.16, y_centro + 0.012, titulo_fila, fontsize=9.3,
                     fontweight='bold', ha='left', va='center')
            ax.text(0.16, y_centro - 0.028, sub, fontsize=8, color='dimgray',
                     ha='left', va='center', wrap=True)

        ax.set_title(titulo, fontsize=11, fontweight='bold', loc='left', pad=10)
        ax.text(0.0, 1.02, 'Pasa el mouse sobre una fila: esa parte\n'
                            'del grafico empieza a parpadear.',
                fontsize=7.6, color='dimgray', ha='left', va='bottom',
                style='italic', transform=ax.transAxes)

    # -----------------------------------------------------------------
    def registrar_badge(self, num, artista_texto):
        """Asocia el numero de leyenda con su marcador numerado sobre el
        grafico principal (el circulo con el numero adentro)."""
        self.badges[num] = artista_texto

    def registrar_halo(self, num, artista_o_lista):
        """Asocia el numero de leyenda con el/los artista(s) 'halo'
        (creados ocultos, visible=False) que deben aparecer parpadeando
        sobre el grafico principal cuando el mouse este sobre esa fila."""
        lista = self.halos.setdefault(num, [])
        if isinstance(artista_o_lista, (list, tuple)):
            lista.extend(artista_o_lista)
        else:
            lista.append(artista_o_lista)

    # -----------------------------------------------------------------
    def _on_motion(self, event):
        if event.inaxes is self.ax_leyenda and event.ydata is not None:
            encontrado = None
            for num, y_centro in self.leyenda_y.items():
                if abs(event.ydata - y_centro) <= self.fila_alto / 2:
                    encontrado = num
                    break
            self.hover_num = encontrado
        else:
            self.hover_num = None

    def _aplicar_parpadeo(self, num_activo, encendido):
        for num in self.numeros:
            activo = (num == num_activo)
            mostrar = activo and encendido

            self.rects[num].set_alpha(0.45 if mostrar else (0.12 if activo else 0.0))
            self.scatters[num].set_sizes([560] if mostrar else [420])

            badge = self.badges.get(num)
            if badge is not None:
                bbox_patch = badge.get_bbox_patch()
                if bbox_patch is not None:
                    if mostrar:
                        bbox_patch.set_edgecolor('#FFE14D')
                        bbox_patch.set_linewidth(3.2)
                    else:
                        bbox_patch.set_edgecolor('black')
                        bbox_patch.set_linewidth(0.6)

            # set_visible(False) evita que Matplotlib dibuje el halo por
            # completo cuando esta apagado (mas rapido que dejarlo con
            # alpha=0, que igual se procesa en cada redibujado).
            for halo in self.halos.get(num, []):
                halo.set_visible(mostrar)

    def _blink_tick(self):
        self._blink_on = not self._blink_on
        if self.hover_num is None and self._ultimo_num is None:
            return  # nada que mostrar ni que apagar: no se pide redibujado
        self._aplicar_parpadeo(self.hover_num,
                                self._blink_on if self.hover_num is not None else False)
        self._ultimo_num = self.hover_num
        self.fig.canvas.draw_idle()

    def iniciar_parpadeo(self, interval=180):
        """Arranca el timer de parpadeo (liviano: solo hace algo cuando el
        mouse esta realmente sobre la leyenda). Hay que conservar una
        referencia a este objeto (o al timer) para que no se destruya."""
        self.timer = self.fig.canvas.new_timer(interval=interval)
        self.timer.add_callback(self._blink_tick)
        self.timer.start()
        return self.timer
