from dataclasses import dataclass

@dataclass
class SectionAssigment:
	first_section: int
	last_section : int

	@staticmethod
	def from_text(text: str):
		''' Retrieve a SectionAssigment from it's text definition
		
		>>> SectionAssigment.from_text('2-4')
		SectionAssigment(first_section=2, last_section=4)
		'''
		first_section, last_section = text.split('-')
		return SectionAssigment(int(first_section), int(last_section))

@dataclass
class PairedAssigments:
	a: SectionAssigment
	b: SectionAssigment

	@staticmethod
	def from_text(text: str):
		''' Retrieve a PairedAssigments from it's text definition
		
		>>> PairedAssigments.from_text('2-4,6-8')
		PairedAssigments(a=SectionAssigment(first_section=2, last_section=4), b=SectionAssigment(first_section=6, last_section=8))
		'''
		a, b = text.split(',')
		return PairedAssigments(
			SectionAssigment.from_text(a),
			SectionAssigment.from_text(b)
		)

	def fully_overlap(self):
		''' Check if one of the assigment is fully contained by the other
		
		>>> PairedAssigments(SectionAssigment(2, 4), SectionAssigment(6, 8)).fully_overlap()
		False
		>>> PairedAssigments(SectionAssigment(2, 3), SectionAssigment(4, 5)).fully_overlap()
		False
		>>> PairedAssigments(SectionAssigment(5, 7), SectionAssigment(7, 9)).fully_overlap()
		False
		>>> PairedAssigments(SectionAssigment(2, 8), SectionAssigment(3, 7)).fully_overlap()
		True
		>>> PairedAssigments(SectionAssigment(6, 6), SectionAssigment(4, 6)).fully_overlap()
		True
		>>> PairedAssigments(SectionAssigment(2, 6), SectionAssigment(4, 8)).fully_overlap()
		False
		'''
		if self.a.first_section <= self.b.first_section <= self.b.last_section <= self.a.last_section:
			return True

		if self.b.first_section <= self.a.first_section <= self.a.last_section <= self.b.last_section:
			return True

		return False

	def partial_overlap(self):
		''' Check if one of the assigment overlap with the other
		
		>>> PairedAssigments(SectionAssigment(2, 4), SectionAssigment(6, 8)).partial_overlap()
		False
		>>> PairedAssigments(SectionAssigment(2, 3), SectionAssigment(4, 5)).partial_overlap()
		False
		>>> PairedAssigments(SectionAssigment(5, 7), SectionAssigment(7, 9)).partial_overlap()
		True
		>>> PairedAssigments(SectionAssigment(2, 8), SectionAssigment(3, 7)).partial_overlap()
		True
		>>> PairedAssigments(SectionAssigment(6, 6), SectionAssigment(4, 6)).partial_overlap()
		True
		>>> PairedAssigments(SectionAssigment(2, 6), SectionAssigment(4, 8)).partial_overlap()
		True
		'''
		if self.a.first_section <= self.b.first_section <= self.a.last_section:
			return True

		if self.a.first_section <= self.b.last_section <= self.a.last_section:
			return True

		if self.b.first_section <= self.a.first_section <= self.b.last_section:
			return True

		if self.b.first_section <= self.a.last_section <= self.b.last_section:
			return True

		return False

if __name__ == '__main__':
	import doctest
	doctest.testmod()