from pupa.scrape import Scraper, Person
import re
import lxml.html


def get_field(doc, key):
    # get text_content of parent of the element containing the key
    elem = doc.xpath('//div[@id="member-info"]/p/strong[text()="%s"]/..' % key)
    if elem:
        return elem[0].text_content().replace(key, '').strip()
    else:
        return ''


class DCPersonScraper(Scraper):

    def scrape(self):
        council_url = 'http://dccouncil.us/council'
        data = self.get(council_url).text
        doc = lxml.html.fromstring(data)
        doc.make_links_absolute(council_url)
        # page should have 13 unique council URLs
        urls = set(doc.xpath('//a[contains(@href, "dccouncil.us/council/")]/@href'))
        # print '\n'.join(urls)
        assert len(urls) <= 13, "should have 13 unique councilmember URLs"

        for url in urls:
            data = self.get(url).text
            doc = lxml.html.fromstring(data)
            doc.make_links_absolute(url)

            descriptor = doc.xpath('//p[@class="head-descriptor"]/text()')[0]
            title_name = doc.xpath('//h2/text()')[0]

            # removes the title that is prepended to the name
            name = re.sub(r'^Councilmember ', '', title_name)

            if 'Chairman' in descriptor:
                district = 'Chairman'
            else:
                district = get_field(doc, 'Represents: ')

            if not district:
                district = 'At-Large'

            # party
            party = get_field(doc, "Political Affiliation:")
            if 'Democratic' in party:
                party = 'Democratic'
            else:
                party = 'Independent'

            photo_url = doc.xpath('//div[@id="member-thumb"]/img/@src')
            if photo_url:
                photo_url = photo_url[0]
            else:
                photo_url = ''

            office_address = get_field(doc, "Office:")
            phone = get_field(doc, "Tel:")
            if phone.endswith('| Fax:'):
                fax = None
                phone = phone.strip('| Fax:') or None
            else:
                phone, fax = phone.split(' | Fax: ')

            email = doc.xpath('//a[starts-with(text(), "Send an email")]/@href')[0].split(':')[1]

            person = Person(
                name=name,
                party=party,
                image=photo_url,
                primary_org='legislature',
                district=str(district),
            )

            person.add_source(url)
            person.add_link(url)

            if office_address:
                person.add_contact_detail(type='address', value=office_address,
                                          note='Capitol Office')
            if phone:
                person.add_contact_detail(type='voice', value=phone,
                                          note='Capitol Office')
            if fax:
                person.add_contact_detail(type='fax', value=fax,
                                          note='Capitol Office')
            if email:
                person.add_contact_detail(type='email', value=email,
                                          note='Capitol Office')

            yield person
