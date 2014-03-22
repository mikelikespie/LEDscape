/** \file
 * Test the ledscape library by pulsing RGB on the first three LEDS.
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <time.h>
#include <inttypes.h>
#include <errno.h>
#include <unistd.h>
#include <math.h>
#include "ledscape.h"

static void
ledscape_fill_color(
	ledscape_frame_t * const frame,
	const unsigned num_pixels,
	const uint8_t r,
	const uint8_t g,
	const uint8_t b
)
{
	for (unsigned i = 0 ; i < num_pixels ; i++)
		for (unsigned strip = 0 ; strip < LEDSCAPE_NUM_STRIPS ; strip++)
			ledscape_set_color(frame, strip, i, r, g, b);
}


int main (void)
{
	const int num_pixels = 256;
	ledscape_t * const leds = ledscape_init(num_pixels);
	time_t last_time = time(NULL);
	unsigned last_i = 0;

	unsigned i = 0;
	while (1)
	{
		// Alternate frame buffers on each draw command
		const unsigned frame_num = i++ % 2;
		ledscape_frame_t * const frame
			= ledscape_frame(leds, frame_num);

		uint8_t val = i >> 1;
		uint16_t r = ((i >>  0) & 0xFF);
		uint16_t g = ((i >>  8) & 0xFF);
		uint16_t b = ((i >> 16) & 0xFF);
		//ledscape_fill_color(frame, num_pixels, val, val, val);

		unsigned lit_strip = last_time % LEDSCAPE_NUM_STRIPS;

		clock_t clk = clock();
		for (unsigned strip = 0 ; strip < LEDSCAPE_NUM_STRIPS ; strip++)
		{
			for (unsigned p = 0 ; p < num_pixels ; p++)
			{
				int segment = p / 16;
				int pos_in_segment = p % 16;
#if 0
				int r = lit_strip  == strip ? 127 : ((p + last_time) % 16) * 8;
				int g = lit_strip  == strip ? 127 : ((p + 5 + last_time) % 16) * 8;
				int b = lit_strip  == strip ? 127 : ((p  + 12 + last_time) % 16) * 8;
#else
				int brightness = (1.0 + sinf(clk / (float)(CLOCKS_PER_SEC))) * 64;

				int r = segment % 3 == 0 ? brightness : 0;
				int g = segment % 3 == 1 ? brightness : 0;
				int b = segment % 3 == 2 ? brightness : 0;
#endif
				ledscape_set_color(
					frame,
					strip,
					p,
#if 0
					((strip % 3) == 0) ? (i) : 0,
					((strip % 3) == 1) ? (i) : 0,
					((strip % 3) == 2) ? (i) : 0

#else
					/*
					(((p/2 + last_time) % 3) == 0) ? brightness : 0,
					(((p/2 + last_time) % 3) == 1) ? brightness : 0,
					(((p/2 + last_time) % 3) == 2) ? brightness : 0
					*/
#endif
					r,
					g,
					b
				);
				//ledscape_set_color(frame, strip, 3*p+1, 0, p+val + 80, 0);
				//ledscape_set_color(frame, strip, 3*p+2, 0, 0, p+val + 160);
			}
		}

		// wait for the previous frame to finish;
		const uint32_t response = ledscape_wait(leds);
		time_t now = time(NULL);
		if (now != last_time)
		{
			printf("%d fps. starting %d previous %"PRIx32"\n",
				i - last_i, i, response);
			last_i = i;
			last_time = now;
			printf("%ld\n", last_time % LEDSCAPE_NUM_STRIPS);
		}

		ledscape_draw(leds, frame_num);
	}

	ledscape_close(leds);

	return EXIT_SUCCESS;
}
