package nl.avisi.kitea.rest;

import com.atlassian.confluence.pages.AbstractPage;
import com.atlassian.confluence.pages.PageManager;
import com.atlassian.confluence.user.ConfluenceUserManager;
import com.atlassian.confluence.user.persistence.dao.ConfluenceUserDao;
import com.atlassian.plugin.spring.scanner.annotation.imports.ConfluenceImport;

import javax.inject.Inject;
import javax.inject.Named;
import java.util.Iterator;

@Named
public class FetchUserHistory {
    @ConfluenceImport
    private final PageManager pageManager;


    @Inject
    public FetchUserHistory(PageManager pageManager) {
        this.pageManager = pageManager;
    }

    public String fetch(String username) {
        Iterator userHistory = this.pageManager.getRecentlyModifiedEntitiesForUser(username);
        while(userHistory.hasNext()) {
            System.out.println(userHistory.next());
        }

        return("");
    }
}
