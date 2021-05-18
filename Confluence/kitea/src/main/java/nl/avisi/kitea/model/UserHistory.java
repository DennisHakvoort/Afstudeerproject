package nl.avisi.kitea.model;

import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlRootElement;

@XmlRootElement
public class UserHistory {
    @XmlElement
    private String key;

    @XmlElement
    private String message;

    public UserHistory() {
    }

    public UserHistory(String key, String message) {
       this.key = key;
       this.message = message;
    }

    public String getMessage() {
        return message;
    }

    public void setMessage(String message) {
        this.message = message;
    }

    public String getKey() {
       return key;
    }

    public void setKey(String key) {
       this.key = key;
    }
}