+++
title = "Hello world"
date = "2024-02-22T20:10:43-03:00"
author = "Belga, João P"

#
# A brief analysis of current chip context
#
description = "Discussing the landscape of AI and describing why accelerators will be needed for AI's new age"

tags = []
+++

![Imagem de uma FPGA](./images/FPGA.webp)

Last week, we all witnessed how the chip industry has become the real hotspot of the moment. Sam Altman’s statement not only highlighted that our current computational capacity falls short for today's and future AI and complex algorithms, but it also underscored the sobering reality: our projections of enhancing chip processing capacity are, at best, declining rapidly, if not completely stagnating.

Moore’s Law, once a guiding principle, is now outdated.

So, the pressing question emerges: How do we stay on track and continue supporting our growing needs?

In the same speech, Sam Altman provides a swift and straightforward answer: acceleration! To grasp how accelerators will drive the next breakthrough in computational requirements, we must first understand how we’ve managed to enhance our processing capacity.

Since the inception of CMOS transistors, the underlying technology in chips has remained fundamentally the same. While we’ve made algorithmic advancements, the heart of processors still beats with CMOS transistors, arranged in various configurations to handle logical and arithmetic tasks. Our strategy for boosting processing capacity has primarily involved shrinking transistor sizes. Put simply, halving the transistor size within the same circuit area doubles the quantity and, consequently, the processing capacity. However, we’re now approaching physical limits.

Enter accelerators—not to shrink transistors further, but to introduce purpose-built processors that can’t function independently. Instead, they work in tandem with a host responsible for managing tasks. The most widely used accelerator? Clearly, GPUs. Yet, GPUs come with drawbacks: they’re costly in terms of materials and energy consumption, which makes them not viable for many applications.

And this is the problem we at Balleb are **currently addressing**.

Operating within strict boundaries and specific requirements does limit our solutions. However, this limitation doesn't necessarily pose a problem. In fact, constrained solutions often prove to be more efficient. By designing processors for specific purposes, we reduce the need for extensive area and logic elements, resulting in lower energy consumption. But there's a catch: popularizing ASICs (Application-Specific Integrated Circuits) remains challenging due to their high cost. 

ASICs for edge AI will come, but we don't have to wait: enter **softcores**! 

This represents our initial steps—the "Hello World" of Balleb's journey.