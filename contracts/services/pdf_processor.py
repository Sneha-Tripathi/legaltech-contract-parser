import fitz

from contracts.services.logger import logger





class PDFProcessor:



    def __init__(self,pdf_path):


        self.pdf_path = pdf_path


        try:


            self.doc = fitz.open(pdf_path)


            logger.info(

                f"Loaded PDF : {pdf_path}"

            )



        except Exception as e:



            logger.error(


                f"{e}"

            )


            raise





    def get_metadata(self):



        logger.info(

            "Metadata Extracted"

        )


        return self.doc.metadata





    def get_page_count(self):



        return len(self.doc)





    def extract_text(self):



        text=""


        try:



            for page in self.doc:



                text += page.get_text()



            logger.info(

                "Text Extraction Success"

            )


            return text




        except Exception as e:



            logger.error(

                f"{e}"

            )


            return ""





    def extract_pages(self):



        pages=[]



        for i,page in enumerate(self.doc):



            pages.append(


                {

                    "page":i+1,

                    "text":page.get_text()

                }

            )



        logger.info(

            "Pages Extracted"

        )


        return pages





    def save_text(self):



        text = self.extract_text()



        with open(

                "uploads/day11_output.txt",

                "w",

                encoding="utf-8"

        ) as f:



            f.write(text)



        logger.info(

            "Saved Text"

        )




    def close(self):



        self.doc.close()



        logger.info(

            "Closed PDF"

        )




if __name__=="__main__":



    pdf = PDFProcessor(

        "uploads/sample.pdf"

    )



    print(

        "Pages:",

        pdf.get_page_count()

    )



    print(

        pdf.get_metadata()

    )



    pdf.save_text()



    pdf.close()



    print(

        "Day 11 Completed"

    )
