#include <util/delay.h>
#include "DigitalIO.h"
#include "boards.h"

#include "Serial.h"
#include "SPI.h"

#include "AD7714.h"

using namespace hal;
using namespace hal::bsp;

void adc_init() {
	AD7714_adc.changeChannel(AD7714<AD7714_spi>::AIN3_4_CH);
	_delay_ms(100);
	AD7714_adc.setFilter(AD7714<AD7714_spi>::unipolar, AD7714<AD7714_spi>::Data_24bit, 4000);
}

uint32_t adc_read() {
	AD7714_adc.writeToModeReg(AD7714<AD7714_spi>::SelfCalib, AD7714<AD7714_spi>::Gain_1);
	return AD7714_adc.read_data();
}

void mux_enable_ch(uint8_t ch) {
	mux.disable();
	mux.select(ch);
	mux.enable();
}

constexpr DigitalIO temp_en{12};

int main() {
	Serial0.init(4800);

	temp_en.init(hal::DigitalIO::OUTPUT);
	temp_en.reset();

	mux.init();
	mux.disable();

	analogLDOEnable.init(hal::DigitalIO::OUTPUT);
	analogLDOEnable.set();
	
	AD7714_spi::init();
	AD7714_adc.init();
	
	_delay_ms(5000);

	adc_init();

	/*mux_enable_ch(0);
	mux.enable();
	temp_en.set();
	while(1) {}*/
	
	while(1) {
		for(int i = 1; i < 4; ++i) {
			mux_enable_ch(i);
			_delay_ms(100);

			uint32_t x = adc_read();

			mux.disable();
			hal::Serial0.printf("0x%08lx ", x);
			_delay_ms(10);
		}
		
		mux_enable_ch(mux_tmp);
		temp_en.set();
		_delay_ms(100);
		uint32_t x = adc_read();

		temp_en.reset();
		hal::Serial0.printf("0x%08lx\r\n", x);
		_delay_ms(10);
	}
	while(1) {}
}
