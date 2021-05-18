package nl.avisi.kitea.model;

import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlRootElement;

@XmlRootElement
public class PageDTO {

    @XmlElement
    private final String document_id;

    @XmlElement
    private final String body;

    @XmlElement
    private final String title;

    @XmlElement
    private final String space;

    public PageDTO(String document_id, String body, String title, String space) {
        this.document_id = document_id;
        this.body = body;
        this.title = title;
        this.space = space;
    }
}
