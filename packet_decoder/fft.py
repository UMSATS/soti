#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# GNU Radio version: 3.10.3.0

from packaging.version import Version as StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import analog
import math
from gnuradio import blocks
from gnuradio import digital
from gnuradio import filter
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import network
from gnuradio import soapy
from gnuradio.qtgui import Range, RangeWidget
from PyQt5 import QtCore



from gnuradio import qtgui

class fft(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("FSK Decoder Backend")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "fft")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.center_freq = center_freq = 435934186
        self.transition_width = transition_width = 10000
        self.ted_gain = ted_gain = 1
        self.squelch = squelch = -50
        self.sample_rate = sample_rate = 2048000
        self.qd_gain = qd_gain = 16
        self.lpf_deci = lpf_deci = 4
        self.low = low = center_freq-5000
        self.loop_bw = loop_bw = 0.0251
        self.high = high = center_freq + 5000
        self.cutoff_freq = cutoff_freq = 50000
        self.constant = constant = -0.02
        self.baud_rate = baud_rate = 9600

        ##################################################
        # Blocks
        ##################################################
        self._qd_gain_range = Range(0, 20, 0.1, 16, 200)
        self._qd_gain_win = RangeWidget(self._qd_gain_range, self.set_qd_gain, "'qd_gain'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._qd_gain_win)
        self._constant_range = Range(-1, 1, 0.01, -0.02, 200)
        self._constant_win = RangeWidget(self._constant_range, self.set_constant, "'constant'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._constant_win)
        self._ted_gain_range = Range(0, 1, 0.01, 1, 200)
        self._ted_gain_win = RangeWidget(self._ted_gain_range, self.set_ted_gain, "'ted_gain'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._ted_gain_win)
        self.soapy_rtlsdr_source_0 = None
        dev = 'driver=rtlsdr'
        stream_args = ''
        tune_args = ['']
        settings = ['']

        self.soapy_rtlsdr_source_0 = soapy.source(dev, "fc32", 1, 'driver=rtlsdr,manufacturer=Realtek,product=RTL2838UHIDIR,soapy=1,tuner=\'Rafael Micro R820T\'',
                                  stream_args, tune_args, settings)
        self.soapy_rtlsdr_source_0.set_sample_rate(0, sample_rate)
        self.soapy_rtlsdr_source_0.set_gain_mode(0, True)
        self.soapy_rtlsdr_source_0.set_frequency(0, center_freq)
        self.soapy_rtlsdr_source_0.set_frequency_correction(0, 0)
        self.soapy_rtlsdr_source_0.set_gain(0, 'TUNER', 20)
        self.qtgui_waterfall_sink_x_0 = qtgui.waterfall_sink_c(
            32768, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            (sample_rate / lpf_deci), #bw
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_waterfall_sink_x_0.set_update_time(0.001)
        self.qtgui_waterfall_sink_x_0.enable_grid(False)
        self.qtgui_waterfall_sink_x_0.enable_axis_labels(True)



        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_0.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_0.set_line_alpha(i, alphas[i])

        self.qtgui_waterfall_sink_x_0.set_intensity_range(-100, -10)

        self._qtgui_waterfall_sink_x_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0.qwidget(), Qt.QWidget)

        self.top_layout.addWidget(self._qtgui_waterfall_sink_x_0_win)
        self.qtgui_time_sink_x_0_0_1_0 = qtgui.time_sink_f(
            10000, #size
            sample_rate, #samp_rate
            "Symbol Sync", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0_0_1_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0_0_1_0.set_y_axis(-2.5, 2.5)

        self.qtgui_time_sink_x_0_0_1_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0_0_1_0.enable_tags(True)
        self.qtgui_time_sink_x_0_0_1_0.set_trigger_mode(qtgui.TRIG_MODE_NORM, qtgui.TRIG_SLOPE_POS, 0.5, 0.0005, 0, "")
        self.qtgui_time_sink_x_0_0_1_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0_0_1_0.enable_grid(False)
        self.qtgui_time_sink_x_0_0_1_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_0_1_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0_0_1_0.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0_0_1_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0_0_1_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_0_1_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_0_1_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_0_1_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_0_1_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_0_1_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_0_1_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0_0_1_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_0_1_0_win)
        self.qtgui_time_sink_x_0_0_0_0 = qtgui.time_sink_f(
            10000, #size
            sample_rate, #samp_rate
            "Final Bits", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0_0_0_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0_0_0_0.set_y_axis(-1.5, 1.5)

        self.qtgui_time_sink_x_0_0_0_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0_0_0_0.enable_tags(True)
        self.qtgui_time_sink_x_0_0_0_0.set_trigger_mode(qtgui.TRIG_MODE_NORM, qtgui.TRIG_SLOPE_NEG, 0.5, 0.0005, 0, "")
        self.qtgui_time_sink_x_0_0_0_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0_0_0_0.enable_grid(False)
        self.qtgui_time_sink_x_0_0_0_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_0_0_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0_0_0_0.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0_0_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0_0_0_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_0_0_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_0_0_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_0_0_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_0_0_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_0_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_0_0_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0_0_0_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_0_0_0_win)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_f(
            10000, #size
            sample_rate, #samp_rate
            "Quadrature Demod Output", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-2, 2)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_NORM, qtgui.TRIG_SLOPE_POS, 1, 0.0005, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_win)
        self.network_udp_sink_0 = network.udp_sink(gr.sizeof_char, 1, '127.0.0.1', 2000, 0, 1024, False)
        self.low_pass_filter_1 = filter.fir_filter_ccf(
            lpf_deci,
            firdes.low_pass(
                1,
                sample_rate,
                cutoff_freq,
                transition_width,
                window.WIN_HAMMING,
                6.76))
        self._loop_bw_range = Range(0, 1, 0.01, 0.0251, 200)
        self._loop_bw_win = RangeWidget(self._loop_bw_range, self.set_loop_bw, "'loop_bw'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._loop_bw_win)
        self.digital_clock_recovery_mm_xx_1 = digital.clock_recovery_mm_ff(((sample_rate/lpf_deci) / baud_rate), (0.25*0.175*0.175), 0.5, 0.175, 0)
        self.digital_binary_slicer_fb_2_0 = digital.binary_slicer_fb()
        self.blocks_uchar_to_float_0_0 = blocks.uchar_to_float()
        self.blocks_pack_k_bits_bb_0 = blocks.pack_k_bits_bb(8)
        self.blocks_add_const_vxx_0 = blocks.add_const_ff(constant)
        self.analog_simple_squelch_cc_1 = analog.simple_squelch_cc((-32), 1)
        self.analog_quadrature_demod_cf_0 = analog.quadrature_demod_cf(qd_gain)
        self.analog_agc_xx_0 = analog.agc_ff((1e-4), 0.6, 0.6)
        self.analog_agc_xx_0.set_max_gain(65536)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_agc_xx_0, 0), (self.digital_clock_recovery_mm_xx_1, 0))
        self.connect((self.analog_quadrature_demod_cf_0, 0), (self.blocks_add_const_vxx_0, 0))
        self.connect((self.analog_simple_squelch_cc_1, 0), (self.analog_quadrature_demod_cf_0, 0))
        self.connect((self.analog_simple_squelch_cc_1, 0), (self.qtgui_waterfall_sink_x_0, 0))
        self.connect((self.blocks_add_const_vxx_0, 0), (self.analog_agc_xx_0, 0))
        self.connect((self.blocks_add_const_vxx_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.blocks_pack_k_bits_bb_0, 0), (self.network_udp_sink_0, 0))
        self.connect((self.blocks_uchar_to_float_0_0, 0), (self.qtgui_time_sink_x_0_0_0_0, 0))
        self.connect((self.digital_binary_slicer_fb_2_0, 0), (self.blocks_pack_k_bits_bb_0, 0))
        self.connect((self.digital_binary_slicer_fb_2_0, 0), (self.blocks_uchar_to_float_0_0, 0))
        self.connect((self.digital_clock_recovery_mm_xx_1, 0), (self.digital_binary_slicer_fb_2_0, 0))
        self.connect((self.digital_clock_recovery_mm_xx_1, 0), (self.qtgui_time_sink_x_0_0_1_0, 0))
        self.connect((self.low_pass_filter_1, 0), (self.analog_simple_squelch_cc_1, 0))
        self.connect((self.soapy_rtlsdr_source_0, 0), (self.low_pass_filter_1, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "fft")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq
        self.set_high(self.center_freq + 5000)
        self.set_low(self.center_freq-5000)
        self.soapy_rtlsdr_source_0.set_frequency(0, self.center_freq)

    def get_transition_width(self):
        return self.transition_width

    def set_transition_width(self, transition_width):
        self.transition_width = transition_width
        self.high_pass_filter_0.set_taps(firdes.high_pass(1, self.sample_rate, 10000, self.transition_width, window.WIN_HAMMING, 6.76))
        self.low_pass_filter_1.set_taps(firdes.low_pass(1, self.sample_rate, self.cutoff_freq, self.transition_width, window.WIN_HAMMING, 6.76))

    def get_ted_gain(self):
        return self.ted_gain

    def set_ted_gain(self, ted_gain):
        self.ted_gain = ted_gain

    def get_squelch(self):
        return self.squelch

    def set_squelch(self, squelch):
        self.squelch = squelch

    def get_sample_rate(self):
        return self.sample_rate

    def set_sample_rate(self, sample_rate):
        self.sample_rate = sample_rate
        self.digital_clock_recovery_mm_xx_1.set_omega(((self.sample_rate/self.lpf_deci) / self.baud_rate))
        self.high_pass_filter_0.set_taps(firdes.high_pass(1, self.sample_rate, 10000, self.transition_width, window.WIN_HAMMING, 6.76))
        self.low_pass_filter_1.set_taps(firdes.low_pass(1, self.sample_rate, self.cutoff_freq, self.transition_width, window.WIN_HAMMING, 6.76))
        self.qtgui_time_sink_x_0.set_samp_rate(self.sample_rate)
        self.qtgui_time_sink_x_0_0_0_0.set_samp_rate(self.sample_rate)
        self.qtgui_time_sink_x_0_0_1_0.set_samp_rate(self.sample_rate)
        self.qtgui_waterfall_sink_x_0.set_frequency_range(0, (self.sample_rate / self.lpf_deci))
        self.soapy_rtlsdr_source_0.set_sample_rate(0, self.sample_rate)

    def get_qd_gain(self):
        return self.qd_gain

    def set_qd_gain(self, qd_gain):
        self.qd_gain = qd_gain
        self.analog_quadrature_demod_cf_0.set_gain(self.qd_gain)

    def get_lpf_deci(self):
        return self.lpf_deci

    def set_lpf_deci(self, lpf_deci):
        self.lpf_deci = lpf_deci
        self.digital_clock_recovery_mm_xx_1.set_omega(((self.sample_rate/self.lpf_deci) / self.baud_rate))
        self.qtgui_waterfall_sink_x_0.set_frequency_range(0, (self.sample_rate / self.lpf_deci))

    def get_low(self):
        return self.low

    def set_low(self, low):
        self.low = low

    def get_loop_bw(self):
        return self.loop_bw

    def set_loop_bw(self, loop_bw):
        self.loop_bw = loop_bw

    def get_high(self):
        return self.high

    def set_high(self, high):
        self.high = high

    def get_cutoff_freq(self):
        return self.cutoff_freq

    def set_cutoff_freq(self, cutoff_freq):
        self.cutoff_freq = cutoff_freq
        self.low_pass_filter_1.set_taps(firdes.low_pass(1, self.sample_rate, self.cutoff_freq, self.transition_width, window.WIN_HAMMING, 6.76))

    def get_constant(self):
        return self.constant

    def set_constant(self, constant):
        self.constant = constant
        self.blocks_add_const_vxx_0.set_k(self.constant)

    def get_baud_rate(self):
        return self.baud_rate

    def set_baud_rate(self, baud_rate):
        self.baud_rate = baud_rate
        self.digital_clock_recovery_mm_xx_1.set_omega(((self.sample_rate/self.lpf_deci) / self.baud_rate))




def main(top_block_cls=fft, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
